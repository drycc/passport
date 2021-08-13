<template>
    <div id="hk-slide-panels">
        <div class="hk-slide-panel-overlay is-visible ember-view">
            <div class="hk-slide-panel-container shadow-outer-2 flex flex-column fixed bg-white overflow-y-hidden ma2 br2 from-right standard" >
                <div class="bg-gradient-silver hk-slide-panel-header relative flex justify-center tc items-center relative bb b--light-silver bg-white z-2 ember-view">
                    <div class="ml4 flex-auto f3 dark-gray truncate lh-copy" >
                        Delete Token
                    </div>
                    <button @click="canelDelete" class="flex bg-transparent bn mr2 mt0 pa1 pointer" type="button">
                        <svg style="height: 16px; width: 16px;" class="icon malibu-icon fill-gray" viewBox="0 0 1024 1024" version="1.1" xmlns="http://www.w3.org/2000/svg" p-id="1158" width="200" height="200"><path d="M574.55 522.35L904.4 192.5c16.65-16.65 16.65-44.1 0-60.75l-1.8-1.8c-16.65-16.65-44.1-16.65-60.75 0L512 460.25l-329.85-330.3c-16.65-16.65-44.1-16.65-60.75 0l-1.8 1.8c-17.1 16.65-17.1 44.1 0 60.75l329.85 329.85L119.6 852.2c-16.65 16.65-16.65 44.1 0 60.75l1.8 1.8c16.65 16.65 44.1 16.65 60.75 0L512 584.9l329.85 329.85c16.65 16.65 44.1 16.65 60.75 0l1.8-1.8c16.65-16.65 16.65-44.1 0-60.75L574.55 522.35z" p-id="1159"></path></svg>
                    </button>
                </div>

                <div class="hk-slide-panel-content relative overflow-y-auto flex flex-column z-1 ember-view">
                    <div class="flex flex-column h-100">
                        <div class="slide-panel-shadow-cover-top z-5"></div>
                        <div class="slide-panel-content flex-grow-1 flex-shrink-0 pa4">
                            <div class="pb3">
                                <div class="ember-view">
                                    <div class="collaborator-edit">
                                        <div class="form-group">
                                            <div class="row">
                                                <div class="col-sm-12">
                                                    <label class="f5 b gray mb2">Do you want delete the Access Token of
                                                      {{ token.token }}
                                                    </label>
                                                    <div class="cp-validating-gravatar-input form-group ember-view">
                                                        <div class="flex flex-auto">
                                                        </div>
                                                    </div>
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                            <button v-if="editAccess" @click="deleteToken" class="w-100 async-button default hk-button--danger ember-view" type="submit">Delete Token</button>
                        </div>
                        <div class="slide-panel-shadow-cover-bottom z-5"></div>
                    </div>
                </div>
                <div class="mh4 ember-view"></div>
                <div class="hk-slide-panel-footer relative shadow-outer-1 flex justify-center items-center z-2 pa4 ember-view">
                    <button @click="canelDelete" class="async-button w-50 mr2 default hk-button--secondary ember-view" type="button">Cancel</button>
                    <button @click="deleteToken" class="async-button w-50 default hk-button--primary ember-view" type="submit">Yes</button>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import AccessTokenDelete from "./AccessTokenDelete"
export default AccessTokenDelete
</script>

<style scoped>

</style>
