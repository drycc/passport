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
{{- if .Values.global.cert_manager_enabled }}
  value: https://drycc.{{ .Values.global.platform_domain }}
{{- else }}
  value: http://drycc.{{ .Values.global.platform_domain }}
{{- end }}
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
  value: {{ .Values.admin_username | default "admin" | quote }}
- name: ADMIN_PASSWORD
  value: {{ .Values.admin_password | default "admin" | quote }}
- name: ADMIN_EMAIL
  value: {{ .Values.admin_email | default "admin@email.com" | quote }}
{{- if eq .Values.global.grafana_location "on-cluster" }}
- name: "DRYCC_MONITOR_GRAFANA_DOMAIN"
{{- if .Values.global.cert_manager_enabled }}
  value: https://drycc-monitor-grafana.{{ .Values.global.platform_domain }}
{{- else }}
  value: http://drycc-monitor-grafana.{{ .Values.global.platform_domain }}
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
{{- if (.Values.database_url) }}
- name: DRYCC_DATABASE_URL
  valueFrom:
    secretKeyRef:
      name: passport-creds
      key: database-url
{{- else if eq .Values.global.database_location "on-cluster" }}
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
- name: DRYCC_DATABASE_NAME
  valueFrom:
    secretKeyRef:
      name: database-creds
      key: passport-database-name
- name: DRYCC_DATABASE_URL
  value: "postgres://$(DRYCC_DATABASE_USER):$(DRYCC_DATABASE_PASSWORD)@$(DRYCC_DATABASE_SERVICE_HOST):$(DRYCC_DATABASE_SERVICE_PORT)/$(DRYCC_DATABASE_NAME)"
{{- end }}
{{- range $key, $value := .Values.environment }}
- name: {{ $key }}
  value: {{ $value | quote }}
{{- end }}
{{- end }}


{{/* Generate passport deployment limits */}}
{{- define "passport.limits" -}}
{{- if or (.Values.limits_cpu) (.Values.limits_memory) }}
resources:
  limits:
{{- if (.Values.limits_cpu) }}
    cpu: {{.Values.limits_cpu}}
{{- end }}
{{- if (.Values.limits_memory) }}
    memory: {{.Values.limits_memory}}
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
