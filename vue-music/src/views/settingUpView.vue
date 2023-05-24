<template>
    <div>
        <el-drawer v-model="props.content.drawer" direction="ltr" size="70%" :with-header="false" :show-close="false">
            <div>
                <div style="text-align: center;">
                    <h3>设置</h3>
                </div>
                <el-divider border-style="dashed" />
                <div>
                    <ul class="ul-style">
                        <li class="li-style" @click="historyRecord = true">历史记录</li>
                        <li class="li-style" @click="deleteHistoryRecord">清除记录</li>
                    </ul>
                </div>
            </div>
        </el-drawer>
    </div>
    <HistoryRecordView :content="historyRecordContent"></HistoryRecordView>
</template>

<script setup lang="ts">
import HistoryRecordView from '@/views/settingUp/HistoryRecordView.vue'
import { ref, reactive } from 'vue'
import { useCounterStore } from '@/stores/counter';
import { ElMessageBox } from "element-plus";
import "element-plus/theme-chalk/el-message-box.css";


const conuter = useCounterStore();

const historyRecord = ref(false);

// defineProps是只读属性，因此最外层无法修改。但和python的列表字典一样，只记录最外层变量的地址，其里面层的地址可以修改
const props = defineProps({
    content: null,
})

const historyRecordContent = reactive({
    drawer: historyRecord,
})

function deleteHistoryRecord() {
    if (conuter.isUser) {
        ElMessageBox.confirm('是否清空历史记录？', '警告', {
            confirmButtonText: '确认',
            cancelButtonText: '取消',
            type: 'warning'
        })
            .then(() => {
                conuter.delete_historyRecord();
                ElMessageBox.alert('成功', '清除记录', { type: 'success' });
            })
            .catch(() => {
                
            })

    } else {
        ElMessageBox.alert('未登录！', '警告', { type: 'warning' });
    }
}

</script>

<style lang='scss' scoped>
@import url("@/assets/css/uili.css");
</style>