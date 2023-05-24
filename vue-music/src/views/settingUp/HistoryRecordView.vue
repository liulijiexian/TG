<template>
    <div>
        <el-drawer v-model="props.content.drawer" direction="btt" size="90%" title="历史记录" :show-close="true">
            <div v-if="!conuter.isUser">未登录！</div>
            <div v-else style="overflow: hidden; height: 100%;">
                <SongListA :content="recordContent" />
            </div>
        </el-drawer>
    </div>
</template>

<script setup lang="ts">
import { useCounterStore } from '@/stores/counter'
import { storeToRefs } from 'pinia';
import { reactive, computed } from 'vue';
import SongListA from '@/components/SongListA.vue';

const conuter = useCounterStore();
const conuterProperty = storeToRefs(conuter);  // 使用 storeToRefs()。它将为每一个响应式属性创建引用。如果调用方法则不需要这个，直接使用conuter就可以了

const props = defineProps({
    content: null,
})

const lsjl = computed(() => {
    return conuterProperty.userInfo.value ? conuterProperty.userInfo.value.data : [];
})

const recordContent = reactive({
    songList: lsjl,  // 歌单
    isImage: false,  // 是否显示图片
    loadingNoMore: true,  // 加载/完毕
    loading: false,  // 加载
    positioning: false,  // 定位
})


</script>

<style lang='scss' scoped></style>