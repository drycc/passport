import { reactive, toRefs } from 'vue'
import { Toast } from "vant";
import {deleteAccessToken} from "../services/tokens";

export default {
    name: "AccessTokenDelete",
    props: {
        token: [Object, Function],
    },
    setup(props, context) {
        const state = reactive({
            token: props.token,
        })

        const canelDelete = () => {
            context.emit('closeDelete', { hasAccessTokenDeleted: false })
        }

        const deleteToken = () => {
            deleteAccessToken(state.token.id).then(res=>{
                if (res.status == 204) {
                    Toast.success("OK")
                    context.emit('closeDelete', { hasAccessTokenDeleted: true })
                }
            })
        }
        return {
            ...toRefs(state),
            canelDelete,
            deleteToken
        }
    }
}
