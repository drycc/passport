<template>
    <div class="ui-footer-shell">
        <div class="ui-footer">
            <div class="ui-footer__content">
                <template v-if="legalEnabled">
                    <ul class="ui-footer__links ui-footer__links--left">
                        <li class="ui-footer__item ui-footer__item--desktop">
                            <a class="ui-footer__link" href="http://www.drycc.com">drycc.com</a>
                        </li>
                        <li class="ui-footer__item">
                            <a class="ui-footer__link" href="https://github.com/drycc">Open Source</a>
                        </li>
                        <li class="ui-footer__item">
                            <a class="ui-footer__link" href="https://drycc.slack.com/">Community</a>
                        </li>
                        <li class="ui-footer__item">
                            <a class="ui-footer__link" href="https://www.drycc.cc/">Documentation</a>
                        </li>
                    </ul>

                    <div class="ui-footer__divider ui-footer__divider--mobile"></div>

                    <div class="ui-footer__support">
                        <a class="ui-footer__support-btn" href="https://tawk.to/chat/6234b5491ffac05b1d7f4669/1fueu8a9t"
                            target="_blank" rel="noopener noreferrer">Support</a>
                    </div>

                    <div class="ui-footer__spacer"></div>

                    <ul class="ui-footer__links ui-footer__links--right">
                        <li class="ui-footer__item">
                            <a class="ui-footer__link"
                                href="https://legal.doopai.com/#/cloud-services-terms">Terms of Service</a>
                        </li>
                        <li class="ui-footer__item">
                            <a class="ui-footer__link"
                                href="https://legal.doopai.com/#/doopai-privacy-policy">Privacy</a>
                        </li>
                        <li class="ui-footer__item">
                            <a class="ui-footer__link"
                                href="https://legal.doopai.com/#/doopai-cookie-policy">Cookies</a>
                        </li>
                        <li class="ui-footer__item ui-footer__copyright">© {{year}} drycc.com</li>
                    </ul>
                </template>
                <template v-else>
                    <ul class="ui-footer__links ui-footer__links--left">
                        <li class="ui-footer__item">
                            <a class="ui-footer__link" href="https://github.com/drycc">Open Source</a>
                        </li>
                        <li class="ui-footer__item">
                            <a class="ui-footer__link" href="https://drycc.slack.com/">Community</a>
                        </li>
                        <li class="ui-footer__item">
                            <a class="ui-footer__link" href="https://www.drycc.cc/">Documentation</a>
                        </li>
                    </ul>

                    <div class="ui-footer__divider ui-footer__divider--mobile"></div>

                    <div class="ui-footer__spacer"></div>

                    <ul class="ui-footer__links ui-footer__links--right">
                        <li class="ui-footer__item">
                            <a class="ui-footer__link"
                                href="https://tawk.to/chat/6234b5491ffac05b1d7f4669/1fueu8a9t">Support</a>
                        </li>
                        <li class="ui-footer__item">
                            <a class="ui-footer__link"
                                href="https://github.com/drycc/workflow/issues">Issues</a>
                        </li>
                        <li class="ui-footer__item ui-footer__copyright">© {{year}} drycc.cc</li>
                    </ul>
                </template>
                <div class="ui-footer__divider ui-footer__divider--mobile"></div>
            </div>
        </div>
    </div>
</template>

<script>
import MainFooter from "./MainFooter"
export default MainFooter
</script>
<style scoped>
.ui-footer {
    width: 100%;
    position: static;
    border-top: 1px solid rgba(217, 226, 239, 0.95);
    background: linear-gradient(180deg, rgba(255, 255, 255, 0.92) 0%, rgba(249, 252, 255, 0.98) 100%);
    backdrop-filter: blur(4px);
}

.ui-footer-shell {
    min-height: 56px;
    margin-top: auto;
    padding-top: 6px;
}

.ui-footer__content {
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 16px;
    display: flex;
    align-items: center;
    gap: 12px;
    min-height: 56px;
    flex-wrap: wrap;
}

.ui-footer__links {
    list-style: none;
    margin: 0;
    padding: 0;
    display: flex;
    align-items: center;
    gap: 16px;
    flex-wrap: wrap;
}

.ui-footer__link {
    color: var(--ui-color-text-secondary);
    text-decoration: none;
    font-size: var(--ui-font-size-sm);
    line-height: 1.35;
    font-weight: var(--ui-font-weight-medium);
    transition: color 0.15s ease;
}

.ui-footer__link:hover {
    color: var(--ui-color-primary);
}

.ui-footer__support {
    margin-left: auto;
}

.ui-footer__support-btn {
    display: inline-block;
    border-radius: 999px;
    padding: 5px 11px;
    font-size: var(--ui-font-size-sm);
    line-height: 1.2;
    font-weight: var(--ui-font-weight-semibold);
    text-decoration: none;
    border: 1px solid var(--ui-color-primary);
    background: var(--ui-color-primary);
    color: #fff;
}

.ui-footer__support-btn:hover {
    background: var(--ui-color-primary-hover);
    border-color: var(--ui-color-primary-hover);
    box-shadow: 0 8px 18px rgba(47, 128, 237, 0.3);
}

.ui-footer__spacer {
    flex: 1;
}

.ui-footer__copyright {
    color: #8a94a6;
    font-size: var(--ui-font-size-sm);
    line-height: 1.35;
}

.ui-footer__divider {
    display: none;
    width: 100%;
    border-top: 1px solid var(--ui-color-border);
}

@media (max-width: 900px) {
    .ui-footer__content {
        min-height: unset;
        padding: 8px 12px;
        gap: 8px;
    }

    .ui-footer__links {
        gap: 12px;
    }

    .ui-footer__link,
    .ui-footer__support-btn,
    .ui-footer__copyright {
        font-size: var(--ui-font-size-xs);
    }

    .ui-footer__support {
        margin-left: 0;
    }

    .ui-footer__spacer {
        display: none;
    }

    .ui-footer__divider--mobile {
        display: block;
    }

    .ui-footer__item--desktop {
        display: none;
    }
}
</style>