<template>
    <div id="aplayer"></div>
</template>
   
<script setup lang="ts">
import APlayer from 'APlayer';
import 'APlayer/dist/APlayer.min.css';
import { useCounterStore } from '@/stores/counter';
import { onMounted, onBeforeUnmount, watchEffect, watch } from 'vue'
import { storeToRefs } from 'pinia'

const conuter = useCounterStore();
const conuterProperty = storeToRefs(conuter);  // 使用 storeToRefs()。它将为每一个响应式属性创建引用。如果调用方法则不需要这个，直接使用conuter就可以了

let ap: any;
let so: any;
let jd: any;
let n = 0;
let ls: any = [];
onMounted(() => {
    // 创建APlayer实例
    so = watchEffect(() => {
        ap = new APlayer({
            container: document.getElementById('aplayer'),
            // autoplay: true,
            listFolded: true,
            lrcType: 2,
            listMaxHeight: '90',
            audio: [],
        });
    });

    jd = watch(conuterProperty.lrclist, () => {
        let a = true;
        if (conuter.isUser) {
            for (let index = 0; index < ls.length; index++) {
                let element = ls[index];
                if (element.url === conuter.nowMusicInfo.url) {
                    ap.list.switch(element.index);
                    a = false
                    break;
                }
            }
        }
        ls.push({ index: ls.length, url: conuter.nowMusicInfo.url });
        if (a) {
            ap.list.add([{
                name: conuter.nowMusicInfo.name,
                artist: conuter.nowMusicInfo.author,
                url: conuter.musicUrl,
                cover: conuter.nowMusicInfo.musicimage,
                lrc: conuter.lrclist,
            }])
            ap.skipForward(); //切换到下一首音频
        }

        if (n === 0) {
            setTimeout(() => {
                const a = <HTMLElement>document.querySelector('.aplayer-pic');
                a.click();
            }, 500);
            n++;
        }
        

    },
        {
            immediate: true,
        }
    )

})


onBeforeUnmount(() => {
    jd();
    so();
    ap.destroy();
})
</script>
   
<style lang='scss'>
#aplayer {
    width: 90vw;
    position: absolute;
    bottom: 10px;
    left: 5vw;
}
</style>