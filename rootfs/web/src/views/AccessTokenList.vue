<!--app列表页-->
<template>
    <nav-bar />
    <div class="limit-width top-nav flex flex-column justify-center">
        <div class="main-content">
            <main-nav :is-access-token-active="true"/>
            <access-token-delete ref="accessTokenDelete" v-if="isShowDelete"
              :token="token"
              @closeDelete="closeDelete"
            />
            <div class="account-nav nav-tabs sub-nav ember-view" style="margin-top: 0px">
                <table class="w-100">
                    <tbody>
                        <tr class="w-100 f5">
                            <th class="pl1 pr1 pv2 bb b--light-gray b">
                                application
                            </th>
                            <th class="pv2 pr1 bb b--light-gray b">
                                token
                            </th>
                            <th class="pv2 pr1 bb b--light-gray b">
                                created
                            </th>
                            <th class="pv2 pr1 bb b--light-gray b">
                                expires
                            </th>
                            <th class="pv2 pr1 bb b--light-gray b">
                            </th>
                        </tr>
                    <template v-for="(token, index) in tokens">
                        <tr class="ember-view">
                            <td class="bb b--light-silver pv2 pr1 gray">{{ token.application }}</td>
                            <td class="bb b--light-silver pv2 pr1 gray">{{ token.token }}</td>
                            <td class="bb b--light-silver pv2 pr1 gray">{{ token.created }}</td>
                            <td class="bb b--light-silver pv2 pr1 gray">{{ token.expires }}</td>
                            <td class="bb b--light-silver action-cell ember-view">
                              <button @click="showDelete(index)" class="bg-transparent hk-focus-ring--blue:focus cursor-hand br1 ba0 b--none pa--1 mr2" title="Delete" type="button" >
                                <span class="clip">Delete</span>
                                <svg style="height: 16px; width: 16px;" class="icon malibu-icon fill-gray hover-fill-red" viewBox="0 0 1024 1024" version="1.1" xmlns="http://www.w3.org/2000/svg" width="200" height="200"><path d="M574.55 522.35L904.4 192.5c16.65-16.65 16.65-44.1 0-60.75l-1.8-1.8c-16.65-16.65-44.1-16.65-60.75 0L512 460.25l-329.85-330.3c-16.65-16.65-44.1-16.65-60.75 0l-1.8 1.8c-17.1 16.65-17.1 44.1 0 60.75l329.85 329.85L119.6 852.2c-16.65 16.65-16.65 44.1 0 60.75l1.8 1.8c16.65 16.65 44.1 16.65 60.75 0L512 584.9l329.85 329.85c16.65 16.65 44.1 16.65 60.75 0l1.8-1.8c16.65-16.65 16.65-44.1 0-60.75L574.55 522.35z" ></path></svg>
                              </button>
                            </td>
                        </tr>
                    </template>
                    </tbody>
                </table>
            </div>
        </div>
    </div>
</template>

<script>
import AccessTokenList from  "./AccessTokenList"
export default AccessTokenList
</script>

<style scoped>
    /*@import "../assets/bashboard.css";*/
    .pr1 {
        padding-right: 15px;
    }
</style>
