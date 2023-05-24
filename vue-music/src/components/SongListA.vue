<template>
    <div class="infinite-list-wrapper list-boxA" @scroll="loadsA">
        <ul :class="classSize">
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
            <span>已经到底咯~~~</span>
        </div>
        <div v-if="dingwei">
            <el-backtop target=".list-boxA" :visibility-height="1" :bottom="90" :right="20">
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
import { ref, reactive, onBeforeUnmount, computed } from 'vue';
import { useCounterStore } from '@/stores/counter';
import { storeToRefs } from 'pinia';
const conuter = useCounterStore();
const conuterProperty = storeToRefs(conuter);  // 使用 storeToRefs()。它将为每一个响应式属性创建引用。如果调用方法则不需要这个，直接使用conuter就可以了

const poprs = defineProps({
    content: null
});

// 歌单容器大小class样式
const classSize = reactive([
    'ul-style'
])


// 歌单class样式
const classList = reactive({
    'li-style': true,
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

const dingwei = ref(false);
function loadsA() {
    if (dingwei.value === false) {
        dingwei.value = true;
    }
}

// 组件注销时
onBeforeUnmount(() => {
    dingwei.value = false;
});
</script>

<style lang='scss' scoped>
// @import url("@/assets/css/songList.css");
@import url("@/assets/css/uili.css");

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