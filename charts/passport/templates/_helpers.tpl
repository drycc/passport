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
- name: TZ
  value: {{ .Values.time_zone | default "UTC" | quote }}
- name: VERSION
  value: {{ .Chart.AppVersion }}
- name: ADMIN_USERNAME
  value: {{ .Values.adminUsername | default "admin" | quote }}
- name: ADMIN_PASSWORD
  value: {{ .Values.adminPassword | default "admin" | quote }}
- name: ADMIN_EMAIL
  value: {{ .Values.adminEmail | default "admin@email.com" | quote }}
- name: PLATFORM_DOMAIN
  value: {{ .Values.global.platformDomain }}
- name: CERT_MANAGER_ENABLED
  value: "{{ .Values.global.certManagerEnabled }}"
{{- if (.Values.valkeyUrl) }}
- name: DRYCC_VALKEY_URL
  valueFrom:
    secretKeyRef:
      name: passport-creds
      key: valkey-url
{{- else if eq .Values.global.valkeyLocation "on-cluster"  }}
- name: VALKEY_PASSWORD
  valueFrom:
    secretKeyRef:
      name: valkey-creds
      key: password
- name: DRYCC_VALKEY_URL
  value: "redis://:$(VALKEY_PASSWORD)@drycc-valkey.{{.Release.Namespace}}.svc.{{.Values.global.clusterDomain}}:16379/1"
{{- end }}
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
  - name: passport-config
    mountPath: /etc/drycc/passport
    readOnly: true
{{- end }}


{{/* Generate passport deployment volumes */}}
{{- define "passport.volumes" }}
volumes:
  - name: passport-creds
    secret:
      secretName: passport-creds
  - name: passport-config
    configMap:
      name: passport-config
{{- end }}
