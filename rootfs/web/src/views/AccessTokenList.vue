<!--app列表页-->
<template>
<div :id="'vue-content-'+Math.random().toString(36).substring(2)">
    <nav-bar />
    <div class="main-panel ui-page-shell">
        <div class="main-content">
            <main-nav :is-access-token-active="true"/>
            <access-token-delete ref="accessTokenDelete" v-if="isShowDelete"
              :token="token"
              @closeDelete="closeDelete"
            />
            <div class="ui-table-wrap">
                <table class="ui-table">
                    <tbody>
                        <tr class="ui-table__head-row">
                            <th>
                                application
                            </th>
                            <th>
                                token
                            </th>
                            <th>
                                created
                            </th>
                            <th>
                                expires
                            </th>
                            <th>
                            </th>
                        </tr>
                    <template v-for="(token, index) in tokens">
                        <tr class="ui-table__body-row">
                            <td>{{ token.application }}</td>
                            <td>{{ token.token }}</td>
                            <td>{{ token.created }}</td>
                            <td>{{ token.expires }}</td>
                            <td class="ui-table__action-cell">
                              <button @click="showDelete(index)" class="ui-icon-btn" title="Delete" type="button" >
                                <span class="clip">Delete</span>
                                <svg style="height: 16px; width: 16px;" class="ui-icon-btn__icon" viewBox="0 0 1024 1024" version="1.1" xmlns="http://www.w3.org/2000/svg" width="200" height="200"><path d="M574.55 522.35L904.4 192.5c16.65-16.65 16.65-44.1 0-60.75l-1.8-1.8c-16.65-16.65-44.1-16.65-60.75 0L512 460.25l-329.85-330.3c-16.65-16.65-44.1-16.65-60.75 0l-1.8 1.8c-17.1 16.65-17.1 44.1 0 60.75l329.85 329.85L119.6 852.2c-16.65 16.65-16.65 44.1 0 60.75l1.8 1.8c16.65 16.65 44.1 16.65 60.75 0L512 584.9l329.85 329.85c16.65 16.65 44.1 16.65 60.75 0l1.8-1.8c16.65-16.65 16.65-44.1 0-60.75L574.55 522.35z" ></path></svg>
                              </button>
                            </td>
                        </tr>
                    </template>
                    <tr v-if="!tokens || tokens.length === 0" class="ui-table__empty-row">
                        <td class="ui-table__empty-cell" colspan="5">
                            <div class="ui-table-empty-state">
                                <div class="ui-table-empty-state__icon" aria-hidden="true"></div>
                                <p class="ui-table-empty-state__title">No access tokens</p>
                                <p class="ui-table-empty-state__desc">Create a token when an integration needs API access.</p>
                            </div>
                        </td>
                    </tr>
                    </tbody>
                </table>
            </div>
        </div>
    </div>
    <main-footer />
</div>
</template>

<script>
import AccessTokenList from  "./AccessTokenList"
export default AccessTokenList
</script>

<style scoped>
.ui-page-shell {
    padding: 14px 0 22px;
}

.ui-table-wrap {
    margin: 14px 16px 18px;
    border: 1px solid rgba(217, 226, 239, 0.95);
    border-radius: 14px;
    background: #ffffff;
    box-shadow: inset 0 0 0 1px rgba(255, 255, 255, 0.65);
    overflow-x: auto;
}

.ui-table {
    width: 100%;
    border-collapse: collapse;
}

.ui-table th,
.ui-table td {
    padding: 12px 14px;
    border-bottom: 1px solid var(--ui-color-border);
    text-align: left;
    color: var(--ui-color-text);
}

.ui-table th {
    text-transform: uppercase;
    letter-spacing: 0.06em;
    font-size: var(--ui-font-size-xs);
    background: var(--ui-color-primary-softer);
    color: #47607f;
        font-weight: var(--ui-font-weight-bold);
}

.ui-table td:nth-child(2) {
    font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, "Liberation Mono", monospace;
    font-size: var(--ui-font-size-xs);
    color: #3b4f69;
}

.ui-table__body-row:hover td {
    background: var(--ui-color-primary-softer);
}

.ui-table__action-cell {
    width: 52px;
}

.ui-table__empty-cell {
    padding: 0;
    border-bottom: none;
}

.ui-table-empty-state {
    min-height: 128px;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: 6px;
    color: var(--ui-color-text-secondary);
    background: transparent;
}

.ui-table-empty-state__icon {
    width: 26px;
    height: 26px;
    border-radius: 999px;
    border: 2px solid #b9cae3;
    position: relative;
}

.ui-table-empty-state__icon::after {
    content: "";
    position: absolute;
    left: 50%;
    top: 50%;
    width: 8px;
    height: 2px;
    margin-left: -4px;
    margin-top: -1px;
    border-radius: 2px;
    background: #8fa8c9;
}

.ui-table-empty-state__title {
    margin: 0;
    font-size: var(--ui-font-size-lg);
        font-weight: var(--ui-font-weight-semibold);
    color: #4f6280;
}

.ui-table-empty-state__desc {
    margin: 0;
    font-size: var(--ui-font-size-sm);
}

.ui-icon-btn {
    border: 1px solid transparent;
    background: #f4f7fc;
    border-radius: var(--ui-radius-sm);
    padding: 5px;
    cursor: pointer;
    transition: all 0.16s ease;
}

.ui-icon-btn__icon {
    fill: #8a94a6;
}

.ui-icon-btn:hover {
    border-color: #fda29b;
    background: #fff5f4;
}

.ui-icon-btn:hover .ui-icon-btn__icon {
    fill: #de0a0a;
}

@media (max-width: 900px) {
    .ui-table-wrap {
        margin: 10px;
    }
}
</style>
