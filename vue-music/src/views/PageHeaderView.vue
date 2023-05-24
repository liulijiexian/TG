<template>
    <div class="header">
        <div class="quf image-div">
            <el-button text style="width: 100%; height: 100%;" @click="drawer = true">
                <el-icon size="20">
                    <EpMenu />
                </el-icon>
            </el-button>
        </div>
        <div class="quf input-div">
            <el-input @keyup.enter="subm" v-model="content" placeholder="请输入歌名/歌手" size="large"
                class="input-style"></el-input>
            <el-button text @click="subm" style="height: 100%;">
                <el-icon>
                    <EpSearch />
                </el-icon>
            </el-button>
        </div>
        <div class="quf user">
            <el-button text style="width: 100%; height: 100%;" @click="login">
                <el-icon size="20">
                    <EpUserFilled />
                </el-icon>
            </el-button>
        </div>
    </div>
    <settingUpView :content="zi_content"></settingUpView>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'
import router from '@/router'
import settingUpView from '@/views/settingUpView.vue'
import { ElMessageBox } from "element-plus";
import "element-plus/theme-chalk/el-message-box.css";
import { useCounterStore } from '@/stores/counter';
const conuter = useCounterStore();

const content = ref('');
const drawer = ref(false);

// 子接收
const zi_content = reactive({
    drawer: drawer,
})

const emit = defineEmits(['sub'])   // 父传递

/**
 * 提交
 */
function subm() {
    if (content.value !== '') {
        emit('sub', content.value);
        content.value = '';
    }


}

/**
 * 登录
 */
function login() {
    if (conuter.isUser) {
        ElMessageBox.confirm(
            '是否退出登录？',
            '警告',
            {
                confirmButtonText: '确认',
                cancelButtonText: '取消',
                type: 'warning'
            }

        )
            .then(() => {
                conuter.delete_login();
                router.push({
                    path: './login'
                });
            })
            .catch(() => {

            })
    }
    else {
        router.push({
            path: './login'
        });
    }

}
</script>

<style lang='scss' scoped>
.header {
    display: flex;
    width: 100%;
    height: 50px;
    border-bottom: 1px solid #ddd;
    justify-content: space-around;

    .quf {
        align-items: center;
        justify-content: center;
        height: 100%;
        text-align: center;
        // vertical-align:middle;

    }

    .image-div {
        width: 50px;
        height: 50px;
    }

    .input-div {
        width: 100%;
        height: 100%;
        display: flex;

        .input-style {
            width: 90%;
            height: 100%;
            font-size: 20px;
        }
    }


    .user {
        width: 50px;
        height: 50px;
    }
}
</style>