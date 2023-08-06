CONSUMER_FILES = {
    "charts/${componentName}/templates/${consumerName}.deploy.yaml": """kind: Deployment
apiVersion: apps/v1
metadata:
  name: {{ template "name" . }}-${consumerName}
  namespace: {{ .Release.Namespace }}
  labels:
    service_name: {{ template "name" . }}-${consumerName}
    release: {{ .Release.Name }}
    app: {{ template "name" . }}-${consumerName}
    version: {{ .Chart.Version }}
    tier: "backend"
spec:
  replicas: {{ .Values.${consumerName}_hpa.minReplicas }}
  revisionHistoryLimit: {{ .Values.revisionHistoryLimit | default "3" }}
  selector:
    matchLabels:
      service_name: {{ template "name" . }}-${consumerName}
      tier: "backend"
  template:
    metadata:
      name: {{ template "name" . }}-${consumerName}
      annotations:
      {{- if .Values.${consumerName}_annotations }}
        checksum/config: {{ include (print $.Template.BasePath "/cm.yaml") . | sha256sum }}
        {{- tpl (toYaml .Values.${consumerName}_annotations) . | nindent 8 }}
      {{- end }}
        prometheus.io/scrape: "true"
        prometheus.io/port: "8080"
      labels:
        service_name: {{ template "name" . }}-${consumerName}
        tier: "backend"
        app: {{ template "name" . }}-${consumerName}
        version: {{ .Chart.Version }}
    spec:
      {{- if .Values.affinity }}
      affinity:
        {{- tpl (toYaml .Values.affinity) . | nindent 8 }}
      {{- end }}
      {{- if .Values.${consumerName}_tolerations }}
      tolerations:
        {{- toYaml .Values.${consumerName}_tolerations | nindent 8 }}
      {{- end }}
      dnsPolicy: ClusterFirst
      {{- if .Values.pullSecrets }}
      imagePullSecrets:
        - name: {{ .Values.pullSecrets }}
      {{- end }}
      containers:
      - name: {{ template "name" . }}-${consumerName}
        image: {{ .Values.image }}
        command: ["${consumerName}"]
        envFrom:
        - configMapRef:
            name: {{ template "name" . }}-config
        {{- if .Values.${consumerName}_resources }}
        resources:
          {{- toYaml .Values.${consumerName}_resources | nindent 10 }}
        {{- end }}
        imagePullPolicy: IfNotPresent
        livenessProbe:
          failureThreshold: 3
          httpGet:
            path: /health
            port: 8080
            scheme: HTTP
          initialDelaySeconds: 60
          periodSeconds: 10
          successThreshold: 1
          timeoutSeconds: 2
        readinessProbe:
          httpGet:
            path: /health
            port: 8080
        ports:
        - name: api
          containerPort: 8080""",
    "charts/${componentName}/templates/${consumerName}.hpa.yaml": """apiVersion: autoscaling/v2beta1
kind: HorizontalPodAutoscaler
metadata:
  name: {{ template "name" . }}-${consumerName}
  namespace: {{ .Release.Namespace }}
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: {{ template "name" . }}-api
  minReplicas: {{ .Values.${consumerName}_hpa.minReplicas }}
  maxReplicas: {{ .Values.${consumerName}_hpa.maxReplicas }}
  metrics:
    {{- toYaml .Values.${consumerName}_hpa.metrics | nindent 4 }}
""",
    "+charts/${componentName}/values.yaml": """${consumerName}_replicaCount: 2
${consumerName}_annotations:
${consumerName}_tolerations: []
${consumerName}_affinity: {}
${consumerName}_resources:
  limits:
    cpu: 1000m
    memory: 512Mi
  requests:
    cpu: 500m
    memory: 256Mi
${consumerName}_hpa:
  minReplicas: 1
  maxReplicas: 2""",
    "${componentName}/${consumerName}.py": """import prometheus_client
from fastapi import APIRouter, FastAPI, Request
from onna_utils.middleware.starlette import PrometheusMiddleware
from starlette.responses import JSONResponse, Response
from onna_utils import metrics
import kafkaesk

router = kafkaesk.Router()

class ConsumerApplication(kafkaesk.Application):
    app_settings: Settings

    def __init__(self, kafka_settings: KafkaSettings, app_settings: Settings):
        super().__init__(
            kafka_servers=kafka_settings.kafka_servers,
            topic_prefix=kafka_settings.kafka_prefix,
            kafka_api_version=kafka_settings.kafka_api_version or "auto",
            kafka_settings=kafka_settings.kafka_settings,
        )
        self.mount(router)
        self.app_settings = app_settings
        self.on("finalize", self._close)

    async def _close(self):
        ...

@router.subscribe(MY_TOPIC, group=MY_GROUP)
async def my_subscriber(my_ob: ObjecType):
    ...


http_router = APIRouter()


@http_router.get("/health")
async def health(request: Request) -> None:
    with metrics.healthy():
		await request.app.consumer.health_check()


@http_router.get("/metrics")
def get_metrics(request: Request) -> Response:
    output = prometheus_client.exposition.generate_latest()
    return Response(output.decode("utf8"))


class HTTPApplication(FastAPI):
    def __init__(self, consumer, *args, **kwargs):
        super().__init__(title="${consumerName}", redoc_url=None, docs_url=None, *args, **kwargs)
        self.add_middleware(PrometheusMiddleware)
        self.include_router(http_router)

		self.consumer = consumer

        self.add_event_handler("startup", self.initialize)
        self.add_event_handler("shutdown", self.finalize)

    async def initialize(self) -> None:
        ...

    async def finalize(self) -> None:
        ...
""",
    "+${componentName}/${componentName}/commands.py": """
def run_${consumerName}():
    settings = get_settings()
    asyncio.run(_run_${consumerName}(settings))


async def _run_${consumerName}(settings: Settings):
	from ${componentName} import ${consumerName}
	from onna_utils.commands import serve_consumer_app

	consumer_app = ${consumerName}.ConsumerApplication()
	http_app = ${consumerName}.HTTPApplication(consumer_app)
	await serve_consumer_app(http_app, consumer_app, port=8080)
""",
    "+${componentName}/pyproject.toml": """
${consumerName} = '${componentName}.commands:run_${consumerName}'
""",
}
