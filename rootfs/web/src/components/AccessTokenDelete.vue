<template>
    <div id="ui-slide-panels">
        <div class="ui-modal-overlay">
            <div class="ui-modal-panel" >
                <div class="ui-modal-header">
                    <div class="ui-modal-title" >
                        Delete Token
                    </div>
                    <button @click="canelDelete" class="ui-modal-close" type="button">
                        <svg style="height: 16px; width: 16px;" class="ui-modal-close__icon" viewBox="0 0 1024 1024" version="1.1" xmlns="http://www.w3.org/2000/svg" p-id="1158" width="200" height="200"><path d="M574.55 522.35L904.4 192.5c16.65-16.65 16.65-44.1 0-60.75l-1.8-1.8c-16.65-16.65-44.1-16.65-60.75 0L512 460.25l-329.85-330.3c-16.65-16.65-44.1-16.65-60.75 0l-1.8 1.8c-17.1 16.65-17.1 44.1 0 60.75l329.85 329.85L119.6 852.2c-16.65 16.65-16.65 44.1 0 60.75l1.8 1.8c16.65 16.65 44.1 16.65 60.75 0L512 584.9l329.85 329.85c16.65 16.65 44.1 16.65 60.75 0l1.8-1.8c16.65-16.65 16.65-44.1 0-60.75L574.55 522.35z" p-id="1159"></path></svg>
                    </button>
                </div>

                <div class="ui-modal-content">
                    <div class="ui-modal-body">
                        <div class="ui-modal-message-wrap">
                            <div>
                                <div>
                                    <div>
                                        <div>
                                            <div>
                                                <div>
                                                    <label class="ui-modal-message">Do you want delete the Access Token of
                                                      {{ token.token }}
                                                    </label>
                                                    <div>
                                                        <div>
                                                        </div>
                                                    </div>
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                            <button v-if="editAccess" @click="deleteToken" class="ui-btn ui-btn--danger ui-btn--block" type="submit">Delete Token</button>
                        </div>
                    </div>
                </div>
                <div class="ui-modal-footer">
                    <button @click="canelDelete" class="ui-btn ui-btn--secondary ui-btn--half" type="button">Cancel</button>
                    <button @click="deleteToken" class="ui-btn ui-btn--primary ui-btn--half" type="submit">Yes</button>
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
.ui-modal-overlay {
    position: fixed;
    inset: 0;
    z-index: 1000;
    background: rgba(15, 23, 42, 0.42);
    display: flex;
    justify-content: flex-end;
}

.ui-modal-panel {
    margin: 12px;
    width: min(520px, calc(100vw - 24px));
    background: #fff;
    border-radius: var(--ui-radius-md);
    box-shadow: var(--ui-shadow-card);
    display: flex;
    flex-direction: column;
    overflow: hidden;
}

.ui-modal-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 14px 16px;
    border-bottom: 1px solid var(--ui-color-border);
}

.ui-modal-title {
    font-size: var(--ui-font-size-3xl);
    font-weight: var(--ui-font-weight-bold);
    color: var(--ui-color-text);
}

.ui-modal-close {
    border: none;
    background: transparent;
    cursor: pointer;
    border-radius: var(--ui-radius-sm);
    padding: 4px;
}

.ui-modal-close__icon {
    fill: #8a94a6;
}

.ui-modal-content {
    padding: 16px;
}

.ui-modal-message {
    display: block;
    color: var(--ui-color-text);
    font-size: var(--ui-font-size-lg);
    font-weight: var(--ui-font-weight-semibold);
    margin-bottom: 10px;
}

.ui-modal-footer {
    display: flex;
    gap: 8px;
    padding: 12px 16px 16px;
    border-top: 1px solid var(--ui-color-border);
}

.ui-btn {
    border-radius: var(--ui-radius-sm);
    border: 1px solid transparent;
    height: 34px;
    padding: 0 14px;
    cursor: pointer;
}

.ui-btn--half {
    width: 50%;
}

.ui-btn--block {
    width: 100%;
}

.ui-btn--primary {
    background: var(--ui-color-primary);
    border-color: var(--ui-color-primary);
    color: #fff;
}

.ui-btn--primary:hover {
    background: var(--ui-color-primary-hover);
    border-color: var(--ui-color-primary-hover);
}

.ui-btn--secondary {
    background: #fff;
    border-color: var(--ui-color-border);
    color: var(--ui-color-text);
}

.ui-btn--secondary:hover {
    border-color: var(--ui-color-primary);
    color: var(--ui-color-primary);
}

.ui-btn--danger {
    background: #fff5f4;
    border-color: #fda29b;
    color: #b42318;
}

.ui-btn--danger:hover {
    background: #d92d20;
    border-color: #d92d20;
    color: #fff;
}

@media (max-width: 900px) {
    .ui-modal-overlay {
        justify-content: center;
        align-items: center;
    }
}

</style>
