<template>
    <div class="infinite-list-wrapper list-box" @scroll="isPositioning">
        <ul v-infinite-scroll="load" :class="classSize" :infinite-scroll-immediate="false">
            <li :class="[classList, { 'li-style-activate': item.url === li_style_activate }]"
                v-for="(item, index) in poprs.content.songList" :key="item.url"
                @click.stop="add_li_style_activate(item, $event)"
                v-memo="[item.url === li_style_activate, item.url]"
                :name="item.url">
                <div style="display: flex;">
                    <div v-if="poprs.content.isImage">
                        <el-image :src="item.musicimage" class="li-image" lazy></el-image>
                    </div>
                    <div style="margin-left: 10px;">
                        <h3 class="title-author">{{ item.name }}</h3>
                        <span class="title-author">{{ item.author?.replace('&', '/') }}</span>
                        <span>{{ item.time }}</span>
                    </div>
                </div>
            </li>
        </ul>
        <div class="loading-noMore">
            <span v-show="poprs.content.loading && poprs.content.loadingNoMore">正在拼命加载中{{ dots }}</span>
            <span v-show="!poprs.content.loadingNoMore">已经到底咯~~~</span>
        </div>
        <div v-if="dingwei">
            <div v-show="positioning" v-if="poprs.content.positioning">
                <el-backtop :bottom="150" :right="20" target=".list-box" :visibility-height="0"
                    @click.prevent.stop="handleClick"  v-show="positioning">
                    <el-tooltip content="定位" placement="top" v-if="positioning">
                        <el-icon style="width: 100%; height: 100%;">
                            <EpPosition />
                        </el-icon>
                    </el-tooltip>
                </el-backtop>
            </div>
            <el-backtop target=".list-box" :visibility-height="1" :bottom="90" :right="20">
                <el-tooltip content="顶部" placement="top">
                    <el-icon style="width: 100%; height: 100%;">
                        <EpTop />
                    </el-icon>
                </el-tooltip>
            </el-backtop>
        </div>
    </div>
</template>

<script setup lang="ts">
import { ref, reactive, onBeforeUnmount, computed, onMounted } from 'vue';
import { useCounterStore } from '@/stores/counter';
import { storeToRefs } from 'pinia';
const conuter = useCounterStore();
const conuterProperty = storeToRefs(conuter);  // 使用 storeToRefs()。它将为每一个响应式属性创建引用。如果调用方法则不需要这个，直接使用conuter就可以了

const poprs = defineProps({
    content: null
});
const emit = defineEmits(['loads'])   // 父传递

// 歌单容器大小class样式
const classSize = reactive([
    'ul-style'
])


const dots = ref('.'); // 初始化字符串
let intervalID: any;
function startDots() {
    // 判断定时器是否为开启状态
    if (intervalID) {
        clearInterval(intervalID);
    }
    dots.value = '.';
    // 使用 setInterval 更新 dots 值，1秒更新一次
    intervalID = setInterval(() => {
        dots.value = dots.value.length < 3 ? dots.value + '.' : '.';
    }, 1000);
}
// startDots();

// 读取音乐信息
function load(e: any) {
    // console.log(poprs.content.loadingNoMore);
    if (!poprs.content.loadingNoMore) {
        if (intervalID) {
            clearInterval(intervalID);
        }
    } else {
        startDots();
        /**
         * 加载数据
        */
        emit('loads');
    }

}

// 歌单class样式
const classList = reactive({
    'li-style': true,
});

// 相对于容器居中位置
const newrePlay = computed(() => {
    // clientHeight：获取当前组件外高度(不包括元素的滚动条和边框，值为number，不是string，即不带px)
    const a = document.getElementsByName(conuterProperty.nowMusicInfo.value.url);
    const listbox = document.getElementsByClassName("list-box");
    const b = a[a.length - 1].offsetTop - listbox[listbox.length - 1].clientHeight / 2;
    return b;
});
// 记录当前 li-style-activate 样式标签index
const li_style_activate = computed(() => {
    if (conuter.nowMusicInfo) {
        return conuterProperty.nowMusicInfo.value.url;
    }
    else {
        return -1;
    }
})


function add_li_style_activate(info: any, e: any) {
    conuter.setNowMusicUid(info);  // 点击播放
}

// 判断滚动条是否在正在播放音乐元素位置
const positioning = ref(false);
function isPositioning() {
    if (li_style_activate.value !== -1) {
        // 如果定位音乐超过了当前显示范围，则出现“定位元素”
        const a = document.getElementsByClassName("list-box");
        const list_box = a[a.length - 1];
        if (Math.abs(list_box.scrollTop - newrePlay.value) > list_box.clientHeight / 2) {
            positioning.value = true;
        } else {
            positioning.value = false;
        }

    }

}
// 缓动函数
function easeInOutCubic(x: number): number {
    return x < 0.5 ? 4 * x * x * x : 1 - Math.pow(-2 * x + 2, 3) / 2;
}
// 回到播放位置
function handleClick() {
    const a = document.getElementsByClassName("list-box");
    const el = a[a.length - 1];
    const beginValue = el.scrollTop;  // 记录点击时滚动条位置
    const beginTime = Date.now();  // 记录开始时间
    
    /**
     * 参考：https://juejin.cn/post/6992958909455532068#heading-13
     * 使用 缓动函数 和 requestAnimationFrame 。
     */
    const rAF = window.requestAnimationFrame || ((func) => setTimeout(func, 16));
    const frameFunc = () => {
        const progress = (Date.now() - beginTime) / 500;  //设置速率 500 毫秒内返回
        if (progress < 1 && beginValue != newrePlay.value) {
            el.scrollTop = beginValue + (newrePlay.value - beginValue) * easeInOutCubic(progress);
            rAF(frameFunc);
        } else {
            // 超过 500 直接返回
            el.scrollTop = newrePlay.value;
            // positioning.value = false;
        }

    }
    rAF(frameFunc);
}

const dingwei = ref(false);
onMounted(() => {
    dingwei.value = true;
})

// 组件注销时 注销intervalID定时器 释放资源
onBeforeUnmount(() => {
    if (intervalID) {
        clearInterval(intervalID);
    }
    dingwei.value = false;
});
</script>

<style lang='scss' scoped>
// @import url("@/assets/css/songList.css");
@import url("@/assets/css/uili.scss");

.infinite-list-wrapper {
    position: relative;
    // display: block;
    height: 90vh;
    // min-width: 100vw;
    overflow-y: scroll;
}


// 设置滚动条样式
.list-box::-webkit-scrollbar {
    width: 10px; // 设置滚动条宽
    opacity: 0;
}

.list-box::-webkit-scrollbar-thumb {
    min-height: 5rem;
    border-radius: 5px; // 滚动条圆角
    // transition: background-color 3s ease-in-out;
    /* 这里设置颜色渐变效果 */
}

.list-box:hover::-webkit-scrollbar-thumb {
    background-color: #ccc; // 滚动条颜色
    opacity: 1;
}

.list-box::-webkit-scrollbar-thumb:hover {
    background-color: #888; // 滚动条颜色
}


// 兼容Firefox、IE
.list-box {
    scrollbar-width: 10px;
    scrollbar-track-color: #ccc;
    scrollbar-color: #ccc
}




.li-style {
    height: 100px;

    div .li-image {
        width: 100px;
        height: 100px;
        min-width: 100px;
        min-height: 100px;
    }

    div h3 {
        margin: 10px 10px 5px 0px;
    }

    div .title-author {
        /* 内容过长显示两行，多余为省略号 */
        text-overflow: ellipsis;
        /*设置隐藏部分为省略号*/
        overflow: hidden;
        /*设置隐藏*/
        display: -webkit-box;
        /*设置显示行数，此处为1行，可设置其他数字*/
        -webkit-line-clamp: 1;
        -webkit-box-orient: vertical;
    }
}

.li-style:hover {
    div h3 {
        color: #409EFF;
    }
}

.li-style-activate {
    background-color: #f3f2f2;

    div h3 {
        color: #409EFF;
    }
}

.li-style+.li-style {
    border-top: 1px solid black;
}



.loading-noMore {
    text-align: center;
    color: #409EFF;
    height: 21px;
}
</style>