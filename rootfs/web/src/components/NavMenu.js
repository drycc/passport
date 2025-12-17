import { markRaw } from "vue";
import { Comment, Document, List, Notebook } from "@element-plus/icons-vue";

export default {
    name: "NavMenu",
    data() {
        return {
            isMenuActived: false,
            resourcesTriggerIcon: markRaw(List),
            resourceItems: [
                {
                    key: "docs",
                    label: "Documentation",
                    href: "https://www.drycc.com",
                    icon: markRaw(Document),
                    external: true
                },
                {
                    key: "community",
                    label: "Community Support",
                    href: "https://www.drycc.cc/community/",
                    icon: markRaw(Comment),
                    external: true
                },
                {
                    key: "blog",
                    label: "Drycc.cc Blog",
                    href: "https://www.drycc.cc/blog/",
                    icon: markRaw(Notebook),
                    external: true
                },
            ]
        }
    }
}
