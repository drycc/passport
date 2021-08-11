<!--app列表页-->
<template>
    <nav-bar />
    <div class="main-panel bg-lightest-silver relative">
        <div class="main-content">
            <div class="collaborator-list limit-width ember-view">
                <table class="w-100 mb5">
                    <tbody>
                        <tr class="w-100 f5">
                            <th class="pl1 pr1 pv2 bb b--light-gray b">
                                application
                            </th>
                            <th class="pv2 pr1 bb b--light-gray b">
                                authorization grant type
                            </th>
                            <th class="pv2 pr1 bb b--light-gray b">
                                user
                            </th>
                            <th class="pv2 pr1 bb b--light-gray b">
                                created
                            </th>
                        </tr>
                    <template v-for="tokens in tokens">
                        <tr class="ember-view">
                            <td class="bb b--light-silver pv2 pr1 gray">{{ tokens.name }}</td>
                            <td class="bb b--light-silver pv2 pr1 gray">{{ tokens.authorization_grant_type }}</td>
                            <td class="bb b--light-silver pv2 pr1 gray">{{ tokens.user }}</td>
                            <td class="bb b--light-silver pv2 pr1 gray">{{ tokens.created }}</td>
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
