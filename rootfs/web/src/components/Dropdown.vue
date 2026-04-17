<template>
    <div
        class="relative inline-block text-left"
        ref="root"
        @focusin="openMenu"
        @focusout="handleFocusOut"
        @mouseenter="handleMouseEnter"
        @mouseleave="handleMouseLeave"
        @keydown.esc="closeMenu"
    >
        <div
            @focus="openMenu"
            @click.stop="openMenu"
            :id="triggerId || undefined"
            :aria-expanded="isOpen ? 'true' : 'false'"
            :aria-controls="menuId || undefined"
            class="outline-none"
            tabindex="0"
        >
            <slot name="trigger">
                <button
                    class="flex items-center gap-2 px-3 py-2 text-sm font-medium text-slate-700 bg-white border border-transparent rounded-lg hover:bg-slate-50 transition-all focus:outline-none group"
                    type="button"
                >
                    <component class="w-4 h-4 text-primary" aria-hidden="true" :is="triggerIcon" />
                    <span :class="{ 'is-mobile-hidden': hideLabelOnMobile }">
                        {{ triggerLabel }}
                    </span>
                </button>
            </slot>
        </div>

        <ul
            :id="menuId || undefined"
            v-show="isOpen" class="absolute right-0 mt-2 z-50 w-56 origin-top-right rounded-xl bg-white shadow-lg ring-1 ring-black/5 focus:outline-none py-1 list-none m-0"
            :class="{ 'ui-top-dropdown__menu--open': isOpen }"
            :style="{ width: normalizedMenuWidth }"
        >
            <li v-if="metaValue" class="">
                <div class="px-4 py-3 border-b border-slate-100">
                    <span class="block text-xs font-medium text-slate-500 mb-0.5">{{ metaLabel || 'Signed in as' }}</span>
                    <span class="block text-sm font-semibold text-slate-800 truncate">{{ metaValue }}</span>
                </div>
            </li>

            <li
                v-for="item in items"
                :key="item.key || item.label"
                class=""
            >
                <a
                    v-if="item.href"
                    class="group flex items-center gap-3 px-4 py-2.5 text-sm text-slate-700 hover:bg-slate-50 hover:text-primary transition-colors w-full text-left"
                    :href="item.href"
                    :target="item.external ? '_blank' : undefined"
                    :rel="item.external ? 'noopener noreferrer' : undefined"
                    @click="handleItemClick(item, $event)"
                >
                    <component v-if="item.icon" class="w-4 h-4 text-slate-400 group-hover:text-primary transition-colors" aria-hidden="true" :is="item.icon" />
                    <span>{{ item.label }}</span>
                </a>

                <button
                    v-else
                    class="group flex items-center gap-3 px-4 py-2.5 text-sm text-slate-700 hover:bg-slate-50 hover:text-primary transition-colors w-full text-left"
                    type="button"
                    @click="handleItemClick(item, $event)"
                >
                    <component v-if="item.icon" class="w-4 h-4 text-slate-400 group-hover:text-primary transition-colors" aria-hidden="true" :is="item.icon" />
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
/* Tailwind handles styles */
</style>
