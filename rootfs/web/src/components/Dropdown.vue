<template>
    <div
        class="ui-top-dropdown"
        ref="root"
        @focusin="openMenu"
        @focusout="handleFocusOut"
        @mouseenter="handleMouseEnter"
        @mouseleave="handleMouseLeave"
        @keydown.esc="closeMenu"
    >
        <button
            :id="triggerId || undefined"
            class="ui-top-dropdown__trigger-button"
            type="button"
            @focus="openMenu"
            @click.stop="openMenu"
            :aria-expanded="isOpen ? 'true' : 'false'"
            :aria-controls="menuId || undefined"
        >
            <el-icon class="ui-top-dropdown__trigger-icon" aria-hidden="true">
                <component :is="triggerIcon" />
            </el-icon>
            <span class="ui-top-dropdown__trigger-label" :class="{ 'is-mobile-hidden': hideLabelOnMobile }">
                {{ triggerLabel }}
            </span>
        </button>

        <ul
            :id="menuId || undefined"
            class="ui-top-dropdown__menu"
            :class="{ 'ui-top-dropdown__menu--open': isOpen }"
            :style="{ width: normalizedMenuWidth }"
        >
            <li v-if="metaValue" class="ui-top-dropdown__item-row">
                <div class="ui-top-dropdown__meta">
                    <span class="ui-top-dropdown__meta-label">{{ metaLabel || 'Signed in as' }}</span>
                    <span class="ui-top-dropdown__meta-value">{{ metaValue }}</span>
                </div>
            </li>

            <li
                v-for="item in items"
                :key="item.key || item.label"
                class="ui-top-dropdown__item-row"
            >
                <a
                    v-if="item.href"
                    class="ui-top-dropdown__link"
                    :href="item.href"
                    :target="item.external ? '_blank' : undefined"
                    :rel="item.external ? 'noopener noreferrer' : undefined"
                    @click="handleItemClick(item, $event)"
                >
                    <el-icon v-if="item.icon" class="ui-top-dropdown__item-icon" aria-hidden="true">
                        <component :is="item.icon" />
                    </el-icon>
                    <span>{{ item.label }}</span>
                </a>

                <button
                    v-else
                    class="ui-top-dropdown__link ui-top-dropdown__link--button"
                    type="button"
                    @click="handleItemClick(item, $event)"
                >
                    <el-icon v-if="item.icon" class="ui-top-dropdown__item-icon" aria-hidden="true">
                        <component :is="item.icon" />
                    </el-icon>
                    <span>{{ item.label }}</span>
                </button>
            </li>
        </ul>
    </div>
</template>

<script>
export default {
    name: "Dropdown",
    props: {
        triggerId: {
            type: String,
            default: ""
        },
        menuId: {
            type: String,
            default: ""
        },
        triggerLabel: {
            type: String,
            required: true
        },
        triggerIcon: {
            type: [Object, Function],
            required: true
        },
        items: {
            type: Array,
            default: () => []
        },
        metaLabel: {
            type: String,
            default: ""
        },
        metaValue: {
            type: String,
            default: ""
        },
        menuWidth: {
            type: [Number, String],
            default: 226
        },
        hideLabelOnMobile: {
            type: Boolean,
            default: false
        },
        closeOnSelect: {
            type: Boolean,
            default: true
        }
    },
    emits: ["action"],
    data() {
        return {
            isOpen: false,
            closeTimer: null
        }
    },
    computed: {
        normalizedMenuWidth() {
            return typeof this.menuWidth === "number" ? `${this.menuWidth}px` : this.menuWidth
        }
    },
    methods: {
        openMenu() {
            this.clearCloseTimer()
            this.isOpen = true
        },
        closeMenu() {
            this.clearCloseTimer()
            this.isOpen = false
        },
        clearCloseTimer() {
            if (this.closeTimer) {
                clearTimeout(this.closeTimer)
                this.closeTimer = null
            }
        },
        handleMouseEnter() {
            this.openMenu()
        },
        handleMouseLeave() {
            this.clearCloseTimer()
            this.closeTimer = setTimeout(() => {
                this.isOpen = false
                this.closeTimer = null
            }, 100)
        },
        handleFocusOut(event) {
            const root = this.$refs.root
            const nextFocused = event.relatedTarget
            if (!root || !nextFocused || !root.contains(nextFocused)) {
                this.closeMenu()
            }
        },
        handleItemClick(item, event) {
            if (item.actionKey) {
                event.preventDefault()
                this.$emit("action", item.actionKey, item)
            }
            if (this.closeOnSelect) {
                this.closeMenu()
            }
        }
    },
    beforeUnmount() {
        this.clearCloseTimer()
    }
}
</script>

<style scoped>
.ui-top-dropdown {
    position: relative;
    display: inline-flex;
    align-items: center;
}

.ui-top-dropdown__trigger-button {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    gap: 6px;
    height: 38px;
    padding: 0 12px;
    border-radius: 9px;
    border: 1px solid transparent;
    background: transparent;
    box-sizing: border-box;
    cursor: pointer;
    text-decoration: none;
    font: inherit;
}

.ui-top-dropdown__trigger-button:hover {
    background: #f5f8fd;
    border-color: #e1e9f5;
}

.ui-top-dropdown__trigger-icon {
    font-size: var(--ui-font-size-3xl);
    color: var(--ui-color-primary);
}

.ui-top-dropdown__trigger-icon :deep(svg),
.ui-top-dropdown__item-icon :deep(svg) {
    stroke-width: 2.4;
    stroke-linecap: round;
    stroke-linejoin: round;
}

.ui-top-dropdown__trigger-label {
    font-size: var(--ui-font-size-xl);
    font-weight: var(--ui-font-weight-semibold);
    color: #4e5e76;
    line-height: 1;
}

.ui-top-dropdown__menu {
    position: absolute;
    right: 0;
    top: calc(100% + 8px);
    padding: 0;
    margin: 0;
    list-style: none;
    background: #fff;
    border: 1px solid rgba(217, 226, 239, 0.96);
    border-radius: 14px;
    box-shadow: 0 16px 36px rgba(16, 42, 72, 0.18);
    overflow: hidden;
    opacity: 0;
    pointer-events: none;
    transform: translateY(-6px);
    transition: all 0.2s ease;
}

.ui-top-dropdown__menu--open {
    opacity: 1;
    pointer-events: auto;
    transform: translateY(0);
}

.ui-top-dropdown__item-row {
    border-bottom: 1px solid var(--ui-color-border);
}

.ui-top-dropdown__item-row:last-child {
    border-bottom: none;
}

.ui-top-dropdown__meta,
.ui-top-dropdown__link {
    display: block;
    padding: 11px 13px;
    text-decoration: none;
    color: var(--ui-color-text);
}

.ui-top-dropdown__meta {
    background: linear-gradient(180deg, #f8fbff 0%, #ffffff 100%);
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    text-align: center;
}

.ui-top-dropdown__meta-label {
    display: block;
    color: #6a7b95;
    font-size: var(--ui-font-size-sm);
}

.ui-top-dropdown__meta-value {
    display: block;
    margin-top: 2px;
    color: #344a66;
    font-size: var(--ui-font-size-md);
    font-weight: var(--ui-font-weight-semibold);
    max-width: 100%;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}

.ui-top-dropdown__link {
    display: flex;
    align-items: center;
    gap: 8px;
    font-size: var(--ui-font-size-lg);
    font-weight: var(--ui-font-weight-medium);
    line-height: var(--ui-line-height-tight);
}

.ui-top-dropdown__link--button {
    width: 100%;
    border: 0;
    background: transparent;
    text-align: left;
    font: inherit;
    cursor: pointer;
}

.ui-top-dropdown__item-icon {
    width: 16px;
    flex: 0 0 16px;
    font-size: var(--ui-font-size-2xl);
    color: var(--ui-color-primary);
}

.ui-top-dropdown__link:hover {
    background: #f4f8fe;
    color: var(--ui-color-primary);
}

.ui-top-dropdown__link:hover .ui-top-dropdown__item-icon {
    color: var(--ui-color-primary);
}

.ui-top-dropdown__item-row:last-child .ui-top-dropdown__link {
    border-radius: 0 0 14px 14px;
}

@media (max-width: 900px) {
    .ui-top-dropdown__trigger-button {
        padding: 0 10px;
        gap: 5px;
    }

    .ui-top-dropdown__trigger-label {
        font-size: var(--ui-font-size-md);
    }

    .ui-top-dropdown__menu {
        width: 208px !important;
    }
}

@media (max-width: 720px) {
    .ui-top-dropdown__trigger-button {
        padding: 0 6px;
    }

    .ui-top-dropdown__trigger-label.is-mobile-hidden {
        display: none;
    }
}
</style>
