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
{{- if (.Values.initGrafanaKey) }}
- name: "DRYCC_GRAFANA_DOMAIN"
{{- if .Values.global.certManagerEnabled }}
  value: https://drycc-monitor-grafana.{{ .Values.global.platformDomain }}
{{- else }}
  value: http://drycc-monitor-grafana.{{ .Values.global.platformDomain }}
{{- end }}
- name: DRYCC_PASSPORT_GRAFANA_KEY
  valueFrom:
    secretKeyRef:
      name: passport-creds
      key: drycc-passport-grafana-key
- name: DRYCC_PASSPORT_GRAFANA_SECRET
  valueFrom:
    secretKeyRef:
      name: passport-creds
      key: drycc-passport-grafana-secret
{{- end }}
{{- if (.Values.initManagerKey) }}
- name: "DRYCC_MANAGER_DOMAIN"
{{- if .Values.global.certManagerEnabled }}
  value: https://drycc-manager.{{ .Values.global.platformDomain }}
{{- else }}
  value: http://drycc-manager.{{ .Values.global.platformDomain }}
{{- end }}
- name: DRYCC_PASSPORT_MANAGER_KEY
  valueFrom:
    secretKeyRef:
      name: passport-creds
      key: drycc-passport-manager-key
- name: DRYCC_PASSPORT_MANAGER_SECRET
  valueFrom:
    secretKeyRef:
      name: passport-creds
      key: drycc-passport-manager-secret
{{- end }}
{{- if (.Values.initControllerKey) }}
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
- name: DRYCC_PASSPORT_CONTROLLER_KEY
  valueFrom:
    secretKeyRef:
      name: passport-creds
      key: drycc-passport-controller-key
- name: DRYCC_PASSPORT_CONTROLLER_SECRET
  valueFrom:
    secretKeyRef:
      name: passport-creds
      key: drycc-passport-controller-secret
{{- end }}
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
{{- if (.Values.databaseUrl) }}
- name: DRYCC_DATABASE_URL
  valueFrom:
    secretKeyRef:
      name: passport-creds
      key: database-url
{{- if (.Values.databaseReplicaUrl) }}
- name: DRYCC_DATABASE_REPLICA_URL
  valueFrom:
    secretKeyRef:
      name: passport-creds
      key: database-replica-url
{{- end }}
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
  value: "postgres://$(DRYCC_DATABASE_USER):$(DRYCC_DATABASE_PASSWORD)@drycc-database.{{.Release.Namespace}}.svc.{{.Values.global.clusterDomain}}:5432/passport"
- name: DRYCC_DATABASE_REPLICA_URL
  value: "postgres://$(DRYCC_DATABASE_USER):$(DRYCC_DATABASE_PASSWORD)@drycc-database-replica.{{.Release.Namespace}}.svc.{{.Values.global.clusterDomain}}:5432/passport"
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
