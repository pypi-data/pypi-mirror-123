SERVICE_FILES = {
    "charts/${componentName}/templates/${serviceName}.deploy.yaml": """kind: Deployment
apiVersion: apps/v1
metadata:
  name: {{ template "name" . }}-${serviceName}
  namespace: {{ .Release.Namespace }}
  labels:
    service_name: {{ template "name" . }}-${serviceName}
    release: {{ .Release.Name }}
    app: {{ template "name" . }}-${serviceName}
    version: {{ .Chart.Version }}
    tier: "backend"
spec:
  replicas: {{ .Values.${serviceName}_hpa.minReplicas }}
  revisionHistoryLimit: {{ .Values.revisionHistoryLimit | default "3" }}
  selector:
    matchLabels:
      service_name: {{ template "name" . }}-${serviceName}
      tier: "backend"
  template:
    metadata:
      name: {{ template "name" . }}-${serviceName}
      annotations:
      {{- if .Values.${serviceName}_annotations }}
        checksum/config: {{ include (print $.Template.BasePath "/cm.yaml") . | sha256sum }}
        {{- tpl (toYaml .Values.${serviceName}_annotations) . | nindent 8 }}
      {{- end }}
        prometheus.io/scrape: "true"
        prometheus.io/port: "8080"
      labels:
        service_name: {{ template "name" . }}-${serviceName}
        tier: "backend"
        app: {{ template "name" . }}-${serviceName}
        version: {{ .Chart.Version }}
    spec:
      {{- if .Values.affinity }}
      affinity:
        {{- tpl (toYaml .Values.affinity) . | nindent 8 }}
      {{- end }}
      {{- if .Values.${serviceName}_tolerations }}
      tolerations:
        {{- toYaml .Values.${serviceName}_tolerations | nindent 8 }}
      {{- end }}
      dnsPolicy: ClusterFirst
      {{- if .Values.pullSecrets }}
      imagePullSecrets:
        - name: {{ .Values.pullSecrets }}
      {{- end }}
      containers:
      - name: {{ template "name" . }}-${serviceName}
        image: {{ .Values.image }}
		command: ["${serviceName}"]
        envFrom:
        - configMapRef:
            name: {{ template "name" . }}-config
        {{- if .Values.${serviceName}_resources }}
        resources:
          {{- toYaml .Values.${serviceName}_resources | nindent 10 }}
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
    "charts/${componentName}/templates/${serviceName}.hpa.yaml": """apiVersion: autoscaling/v2beta1
kind: HorizontalPodAutoscaler
metadata:
  name: {{ template "name" . }}-${serviceName}
  namespace: {{ .Release.Namespace }}
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: {{ template "name" . }}-api
  minReplicas: {{ .Values.${serviceName}_hpa.minReplicas }}
  maxReplicas: {{ .Values.${serviceName}_hpa.maxReplicas }}
  metrics:
    {{- toYaml .Values.${serviceName}_hpa.metrics | nindent 4 }}
""",
    "charts/${componentName}/templates/${serviceName}.svc.yaml": """kind: Service
apiVersion: v1
metadata:
  name: {{ template "name" . }}-${serviceName}
  namespace: {{ .Release.Namespace }}
  labels:
    service_name: {{ template "name" . }}-${serviceName}
    app: {{ template "name" . }}-${serviceName}
    version: {{ .Chart.Version }}
    tier: "backend"
    release: {{ .Release.Name }}
  annotations:
    getambassador.io/config: |
      ---
      apiVersion: ambassador/v1
      kind:  Mapping
      name:  ambassador_{{ template "name" . }}_${serviceName}_{{ .Release.Namespace | default .Values.app }}_mapping
      prefix: /${serviceName}/
      service: {{ template "name" . }}-${serviceName}.{{ .Release.Namespace | default .Values.app }}:8080
      resolver: endpoint
      timeout_ms: 600000
      connect_timeout_ms: 30000
      idle_timeout_ms: 60000
      circuit_breakers:
      - priority: default
        max_connections: 3072
        max_pending_requests: 2048
        max_requests: 4096
        max_retries: 50
      load_balancer:
        policy: round_robin
      retry_policy:
        retry_on: gateway-error
        num_retries: 4
spec:
  type: ClusterIP
  ports:
  - name: http
    port: 8080
    targetPort: 8080
  selector:
    service_name: {{ template "name" . }}-${serviceName}
""",
    "+charts/${componentName}/values.yaml": """${serviceName}_replicaCount: 2
${serviceName}_annotations:
${serviceName}_tolerations: []
${serviceName}_affinity: {}
${serviceName}_resources:
  limits:
    cpu: 1000m
    memory: 512Mi
  requests:
    cpu: 500m
    memory: 256Mi""",
    "${componentName}/${serviceName}.py": """import prometheus_client
from fastapi import APIRouter, FastAPI, Request
from onna_utils.middleware.starlette import PrometheusMiddleware
from starlette.responses import JSONResponse, Response

router = APIRouter()


@router.get("/health")
async def health(request: Request) -> None:
    ...


@router.get("/metrics")
def get_metrics(request: Request) -> Response:
    output = prometheus_client.exposition.generate_latest()
    return Response(output.decode("utf8"))


@router.get("/ping")
def get_ping(request: Request) -> Response:
    return JSONResponse({"po": "ng"})


@router.get("/foobar")
async def get_foobar():
    return {}


class HTTPApplication(FastAPI):
    def __init__(
        self,
        *args,
        **kwargs,
    ):
        super().__init__(title="${serviceName}", redoc_url=None, docs_url=None, *args, **kwargs)
        self.add_middleware(PrometheusMiddleware)
        self.include_router(router)

        self.add_event_handler("startup", self.initialize)
        self.add_event_handler("shutdown", self.finalize)

    async def initialize(self) -> None:
        ...

    async def finalize(self) -> None:
        ...
""",
    "+${componentName}/${componentName}/commands.py": """
def run_${serviceName}():
    settings = get_settings()
    asyncio.run(_run_${serviceName}(settings))


async def _run_${serviceName}(settings: Settings):
	from ${componentName} import ${serviceName}
	import uvicorn

    http_config = uvicorn.Config(
        ${serviceName}.HTTPApplication(),
        port=8080,
        host="0.0.0.0",
        log_level=None,
    )
    server = uvicorn.Server(config=http_config)
    await server.serve()
""",
    "+${componentName}/pyproject.toml": """
${serviceName} = '${componentName}.commands:run_${serviceName}'
""",
}
