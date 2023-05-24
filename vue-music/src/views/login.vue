<template>
    <div class="login">
        <Transition v-show="entrance" name="slide-fade">
            <div>
                <div class="main">
                    <div class="title">
                        <h1>Login</h1>
                    </div>
                    <div class="user">
                        <div>
                            <b>注意：未注册账号会自动注册，请仔细检测需要登录账号是否正确</b>
                        </div>
                        <br />
                        <br />
                        <br />
                        <div>
                            <div class="uid">
                                <el-icon>
                                    <EpUserFilled />
                                </el-icon>
                            </div>
                            <input @keyup.enter="sub" class="input" v-model="content" placeholder="请输入账号" />
                        </div>
                    </div>
                    <br />
                    <div class="button">
                        <div class="login-button-div">
                            <el-button class="login-button" round @click="sub">登录</el-button>
                        </div>
                    </div>
                </div>
                <div class="back">
                    <el-icon @click="onBack">
                        <EpBack />
                    </el-icon>
                </div>
            </div>
        </Transition>


    </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from "vue";
import { useCounterStore } from '@/stores/counter';
import router from '@/router'
import { ElMessageBox } from "element-plus";
import "element-plus/theme-chalk/el-message-box.css";

const conuter = useCounterStore();
const content = ref('');

const entrance = ref(false);  // 是否进入页面

/**
 * 登录
 */
function sub() {
    if (content.value === '' || content.value.length < 6) {
        ElMessageBox.alert('账号不能为空或小于6位', '警告', { type: 'warning' });
    } else {
        conuter.get_login(content.value);
        setTimeout(() => {
            if (conuter.isUser) {
                onBack();
            }
            else {
                ElMessageBox.alert('登陆失败，请重新登陆', '警告', { type: 'warning' });
            }
        }, 500)

    }

}

/**
 * 回到首页
 */
function onBack() {
    entrance.value = false;
    setTimeout(() => {
        router.push({
            path: '/'
        });
    }, 600);

}

onMounted(() => {
    entrance.value = true;
})

</script>

<style lang='scss' scoped>
/*
  进入和离开动画可以使用不同
  持续时间和速度曲线。
*/
.slide-fade-enter-active {
    transition: all 1s cubic-bezier(0, 0.3, 0.8, 1);
}

.slide-fade-leave-active {
    transition: all 0.6s cubic-bezier(0, 0.3, 0.8, 1);
}

.slide-fade-enter-from,
.slide-fade-leave-to {
    transform: translateX(3em);
    opacity: 0;
}


.login {
    margin: 0 0 -8px -8px;
    padding: 0;
    height: 100vh;
    background-image: linear-gradient(to top right, green, pink, #fff);
    background-size: 100%;
    /**执行动画：动画名   时长   线性的   无限次播放 */
    animation: loginBackground 5s linear infinite;
    z-index: 0;
    overflow: hidden;
}

@keyframes loginBackground {
    0% {
        /**背景图片设置初始位置初始值位置 */
        // background-position: 0% 50%;
        filter: hue-rotate(0deg);
    }

    50% {
        // background-position: 100% 50%;
        filter: hue-rotate(180deg);
    }

    100% {
        // background-position: 0% 50%;
        filter: hue-rotate(360deg);
    }
}


.main {
    margin: auto;
    width: 80vw;
    text-align: center;
    overflow: hidden;
    // height: 50vh;
    // z-index: 999;

    .title {
        display: inline-block;
        height: 50vh;
        font-size: 3em;

        h1 {
            display: inline-block;
            vertical-align: middle;
            // -webkit-text-stroke: 3px red;  // 设置字体边框
            color: red; // 颜色透明
        }
    }

    .title::before {
        content: ''; // 伪元素需要加这个才能生效
        width: 0;
        display: inline-block;
        height: 100%;
        vertical-align: middle;
    }

    .user {
        width: 100%;

        /**影响第一层的div，div里嵌套的div不会有影响 */
        >div {
            display: flex;
        }

        .uid {
            margin-top: 8px;
            font-size: 1.5em;
            margin-right: 10px;
        }

        .input {
            width: 80vw;
            height: 2em;
            border: 0;
            outline: none;
            // opacity: 1;
            background: transparent; // 背景透明
            border-bottom: 2px solid black;
            font-size: 20px;
        }
    }

    .button {
        .login-button-div {
            border-radius: 20px;
            overflow: hidden;

            .login-button {
                height: 3em;
                width: 80vw;
            }
        }
    }

}

.back {
    padding: 0;
    margin: 0;
    position: absolute;
    top: 0.5em;
    left: 0.5em;
    color: #fff;
    font-size: 2em;
}

.back:hover {
    cursor: pointer;
}
</style>