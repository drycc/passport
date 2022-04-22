{{/*
Set apiVersion based on .Capabilities.APIVersions
*/}}
{{- define "rbacAPIVersion" -}}
{{- if .Capabilities.APIVersions.Has "rbac.authorization.k8s.io/v1beta1" -}}
rbac.authorization.k8s.io/v1beta1
{{- else if .Capabilities.APIVersions.Has "rbac.authorization.k8s.io/v1alpha1" -}}
rbac.authorization.k8s.io/v1alpha1
{{- else -}}
rbac.authorization.k8s.io/v1
{{- end -}}
{{- end -}}

{{/* Generate passport deployment envs */}}
{{- define "passport.envs" }}
env:
- name: "TZ"
  value: {{ .Values.time_zone | default "UTC" | quote }}
- name: "DRYCC_CONTROLLER_DOMAIN"
{{- if .Values.global.certManagerEnabled }}
  value: https://drycc.{{ .Values.global.platformDomain }}
{{- else }}
  value: http://drycc.{{ .Values.global.platformDomain }}
{{- end }}
- name: DRYCC_SECRET_KEY
  valueFrom:
    secretKeyRef:
      name: passport-creds
      key: django-secret-key
- name: SOCIAL_AUTH_DRYCC_CONTROLLER_KEY
  valueFrom:
    secretKeyRef:
      name: passport-creds
      key: social-auth-drycc-controller-key
- name: SOCIAL_AUTH_DRYCC_CONTROLLER_SECRET
  valueFrom:
    secretKeyRef:
      name: passport-creds
      key: social-auth-drycc-controller-secret
- name: WORKFLOW_NAMESPACE
  valueFrom:
    fieldRef:
      fieldPath: metadata.namespace
- name: ADMIN_USERNAME
  value: {{ .Values.adminUsername | default "admin" | quote }}
- name: ADMIN_PASSWORD
  value: {{ .Values.adminPassword | default "admin" | quote }}
- name: ADMIN_EMAIL
  value: {{ .Values.adminEmail | default "admin@email.com" | quote }}
{{- if eq .Values.global.grafanaLocation "on-cluster" }}
- name: "DRYCC_MONITOR_GRAFANA_DOMAIN"
{{- if .Values.global.certManagerEnabled }}
  value: https://drycc-monitor-grafana.{{ .Values.global.platformDomain }}
{{- else }}
  value: http://drycc-monitor-grafana.{{ .Values.global.platformDomain }}
{{- end }}
- name: GRAFANA_ON_CLUSTER
  value: "true"
- name: SOCIAL_AUTH_DRYCC_GRAFANA_KEY
  valueFrom:
    secretKeyRef:
      name: passport-creds
      key: social-auth-drycc-grafana-key
- name: SOCIAL_AUTH_DRYCC_GRAFANA_SECRET
  valueFrom:
    secretKeyRef:
      name: passport-creds
      key: social-auth-drycc-grafana-secret
{{- end }}
{{- if (.Values.databaseUrl) }}
- name: DRYCC_DATABASE_URL
  valueFrom:
    secretKeyRef:
      name: passport-creds
      key: database-url
{{- else if eq .Values.global.databaseLocation "on-cluster" }}
- name: DRYCC_DATABASE_USER
  valueFrom:
    secretKeyRef:
      name: database-creds
      key: user
- name: DRYCC_DATABASE_PASSWORD
  valueFrom:
    secretKeyRef:
      name: database-creds
      key: password
- name: DRYCC_DATABASE_URL
  value: "postgres://$(DRYCC_DATABASE_USER):$(DRYCC_DATABASE_PASSWORD)@$(DRYCC_DATABASE_SERVICE_HOST):$(DRYCC_DATABASE_SERVICE_PORT)/passport"
{{- end }}
- name: DRYCC_REDIS_ADDRS
  valueFrom:
    secretKeyRef:
      name: redis-creds
      key: addrs
- name: DRYCC_REDIS_PASSWORD
  valueFrom:
    secretKeyRef:
      name: redis-creds
      key: password
{{- range $key, $value := .Values.environment }}
- name: {{ $key }}
  value: {{ $value | quote }}
{{- end }}
{{- end }}


{{/* Generate passport deployment limits */}}
{{- define "passport.limits" -}}
{{- if or (.Values.limitsCpu) (.Values.limitsMemory) }}
resources:
  limits:
{{- if (.Values.limitsCpu) }}
    cpu: {{.Values.limitsCpu}}
{{- end }}
{{- if (.Values.limitsMemory) }}
    memory: {{.Values.limitsMemory}}
{{- end }}
{{- end }}
{{- end }}


{{/* Generate passport deployment volumeMounts */}}
{{- define "passport.volumeMounts" }}
volumeMounts:
  - name: passport-creds
    mountPath: /var/run/secrets/drycc/passport
    readOnly: true
{{- end }}


{{/* Generate passport deployment volumes */}}
{{- define "passport.volumes" }}
volumes:
  - name: passport-creds
    secret:
      secretName: passport-creds
{{- end }}
