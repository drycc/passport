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
{{- else if .Values.valkey.enabled  }}
- name: VALKEY_PASSWORD
  valueFrom:
    secretKeyRef:
      name: valkey-creds
      key: password
- name: DRYCC_VALKEY_URL
  value: "redis://:$(VALKEY_PASSWORD)@drycc-valkey:16379/1"
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
{{- else if .Values.database.enabled }}
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
  value: "postgres://$(DRYCC_DATABASE_USER):$(DRYCC_DATABASE_PASSWORD)@drycc-database:5432/passport"
- name: DRYCC_DATABASE_REPLICA_URL
  value: "postgres://$(DRYCC_DATABASE_USER):$(DRYCC_DATABASE_PASSWORD)@drycc-database-replica:5432/passport"
{{- end }}
{{- range $key, $value := .Values.environment }}
- name: {{ $key }}
  value: {{ $value | quote }}
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

{{/* Generate passport default reserved usernames */}}
{{- define "passport.defaultReservedUsernames" }}
admin
administrator
anonymous
asshole
bastard
billing
callback
cancer
cocaine
contact
coronavirus
cracker
database
developer
doopai
drycc
email
explore
faggot
feedback
hacker
helpdesk
hentai
heroin
hitler
homophobic
horny
idiot
killer
login
logout
moderator
murder
nigger
nigga
official
payment
pedophile
pornhub
profile
racist
rapist
recovery
register
retard
scammer
security
service
settings
sexist
signup
signin
slave
spammer
staff
suicide
support
system
terrorism
trending
undefined
update
username
verification
verify
webmaster
webhook
wetback
whore
xvideos
{{- end }}
