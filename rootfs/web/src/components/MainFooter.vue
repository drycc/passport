<template>
    <div class="outer-footer">
        <div app bottom fixed class="allow-if-delinquent ember-view footer" padless>
            <div class="w-100 flex flex-column flex-row-l items-center bg-white bt b--light-silver ph3-l">
                <template v-if="legalEnabled">
                    <ul class="list flex ma0 pa0 f6 order-0 pv2">
                        <li class="dn flex-l mr3">
                            <a class="hk-link no-underline gray" href="http://www.drycc.com">drycc.com</a>
                        </li>
                        <li class="mr3">
                            <a class="hk-link no-underline gray" href="https://github.com/drycc">Open Source</a>
                        </li>
                        <li class="mr3">
                            <a class="hk-link no-underline gray" href="https://drycc.slack.com/">Community</a>
                        </li>
                        <li class="">
                            <a class="hk-link no-underline gray" href="https://drycc.cc/">Documentation</a>
                        </li>
                    </ul>

                    <div class="bt b--light-silver w-100 dn-l"></div>

                    <div class="flex pv2 ph3 f6 order-5 order-1-l">
                        <a class="hk-button-sm--primary" href="https://tawk.to/chat/6234b5491ffac05b1d7f4669/1fueu8a9t"
                            target="_blank">Support</a>
                    </div>

                    <div class="dn flex-l flex-auto order-3"></div>

                    <ul class="list flex ma0 pa0 pv2 f6 order-2 order-4-l">
                        <li class="">
                            <a class="hk-link no-underline gray"
                                href="https://legal.doopai.com/#/cloud-services-terms">Terms of Service</a>
                        </li>
                        <li class="ml3">
                            <a class="hk-link no-underline gray"
                                href="https://legal.doopai.com/#/doopai-privacy-policy">Privacy</a>
                        </li>
                        <li class="ml3">
                            <a class="hk-link no-underline gray"
                                href="https://legal.doopai.com/#/doopai-cookie-policy">Cookies</a>
                        </li>
                        <li class="ml3 gray">© {{year}} drycc.com</li>
                    </ul>
                </template>
                <template v-else>
                    <ul class="list flex ma0 pa0 f6 order-0 pv2">
                        <li class="mr3">
                            <a class="hk-link no-underline gray" href="https://github.com/drycc">Open Source</a>
                        </li>
                        <li class="mr3">
                            <a class="hk-link no-underline gray" href="https://drycc.slack.com/">Community</a>
                        </li>
                        <li class="">
                            <a class="hk-link no-underline gray" href="https://drycc.cc/">Documentation</a>
                        </li>
                    </ul>

                    <div class="bt b--light-silver w-100 dn-l"></div>

                    <div class="dn flex-l flex-auto order-3"></div>

                    <ul class="list flex ma0 pa0 pv2 f6 order-2 order-4-l">
                        <li class="">
                            <a class="hk-link no-underline gray"
                                href="https://tawk.to/chat/6234b5491ffac05b1d7f4669/1fueu8a9t">Support</a>
                        </li>
                        <li class="ml3">
                            <a class="hk-link no-underline gray"
                                href="https://github.com/drycc/workflow/issues">Issues</a>
                        </li>
                        <li class="ml3 gray">© {{year}} drycc.cc</li>
                    </ul>
                </template>
                <div class="bt b--light-silver w-100 order-4 dn-l"></div>
            </div>
        </div>
    </div>
</template>

<script>
import MainFooter from "./MainFooter"
export default MainFooter
</script>
<style scoped>
.footer {
    width: 100%;
    position: fixed;
    bottom: 0;
}

.outer-footer{
    min-height: 68px;
}
</style>