import axios from "../utils/axios";

export function getOrganizations() {
  return axios.get(`/orgs/`);
}

export function createOrganization(data) {
  return axios.post(`/orgs/`, data);
}

export function getOrganization(name) {
  return axios.get(`/orgs/${name}/`);
}

export function updateOrganization(name, data) {
  return axios.patch(`/orgs/${name}/`, data);
}

export function deleteOrganization(name) {
  return axios.delete(`/orgs/${name}/`);
}

export function getOrganizationMembers(name) {
  return axios.get(`/orgs/${name}/members/`);
}

export function getOrganizationMember(name, username) {
  return axios.get(`/orgs/${name}/members/${username}/`);
}

export function updateOrganizationMemberRole(name, username, role) {
  return axios.patch(`/orgs/${name}/members/${username}/`, { role });
}

export function updateOrganizationMemberAlerts(name, username, alerts) {
  return axios.patch(`/orgs/${name}/members/${username}/`, { alerts });
}

export function removeOrganizationMember(name, username) {
  return axios.delete(`/orgs/${name}/members/${username}/`);
}

export function getOrganizationInvitations(name) {
  return axios.get(`/orgs/${name}/invitations/`);
}

export function createOrganizationInvitation(name, email) {
  return axios.post(`/orgs/${name}/invitations/`, { email });
}

export function getOrganizationInvitation(name, token) {
  return axios.get(`/orgs/${name}/invitations/${token}/`);
}

export function revokeOrganizationInvitation(name, token) {
  return axios.delete(`/orgs/${name}/invitations/${token}/`);
}

export function dealOrganizationList(obj) {
  return obj.data.results.map((item) => {
    return {
      name: item.name,
      email: item.email,
      created: item.created,
      updated: item.updated,
    };
  });
}

export function dealMemberList(obj) {
  return obj.data.results.map((item) => {
    return {
      user: item.user,
      email: item.email,
      organization: item.organization,
      role: item.role,
      alerts: item.alerts || false,
      created: item.created,
      updated: item.updated,
    };
  });
}

export function dealInvitationList(obj) {
  return obj.data.results.map((item) => {
    return {
      email: item.email,
      token: item.token,
      organization: item.organization,
      inviter: item.inviter,
      created: item.created,
      accepted: item.accepted,
    };
  });
}
