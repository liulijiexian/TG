<script setup lang="ts">
import { ref, reactive, computed } from 'vue';
import PageHeaderView from '@/views/PageHeaderView.vue';

import { useCounterStore } from '@/stores/counter';
import { storeToRefs } from 'pinia'

import SongList from '@/components/SongList.vue';
import MediaPlayer from '@/components/MediaPlayer.vue';

const conuter = useCounterStore();
const conuterProperty = storeToRefs(conuter);  // 使用 storeToRefs()。它将为每一个响应式属性创建引用。如果调用方法则不需要这个，直接使用conuter就可以了

const loadingNoMore = computed(() => {
    const isTrue = conuter.musicList.length % 30 === 0;
    return isTrue;
})

const loading = computed(() => {
    return conuter.musicList.length !== 0;
})

const content = reactive({
    songList: conuterProperty.musicList,  // 歌单
    isImage: true,  // 是否显示图片
    loadingNoMore: loadingNoMore,  // 加载/完毕
    loading: loading,  // 加载
    positioning: true,  // 定位
})

let text = ref(''); // 当前搜索的歌名/歌手
let num = 1;  // 页数
function sub(value:string){
    num = 1;  // 初始化页数
    text.value = value;
    continuousSub();
    // conuter.get_Music(text.value, num);
}

/**
 * 请求歌曲列表
 * @param value 
 */
function continuousSub(){
    conuter.get_Music(text.value, num);
    num++;
}

</script>

<template>
  <header>
    <PageHeaderView @sub="sub"></PageHeaderView>
  </header>

  <SongList :content="content" @loads="continuousSub"/>
  <MediaPlayer v-if="conuterProperty.musicUrl.value"></MediaPlayer>
</template>

<style scoped>
header {
  max-height: 100vh;
}

</style>
