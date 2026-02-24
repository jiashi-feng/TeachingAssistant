<template>
  <div class="chat-page">
    <el-card>
      <template #header>
        <span>消息</span>
      </template>
      <div class="chat-layout">
        <div class="conversation-list">
          <div
            v-for="c in conversations"
            :key="c.conversation_id"
            class="conv-item"
            :class="{ active: currentConvId === c.conversation_id }"
            @click="selectConversation(c)"
          >
            <div class="conv-other">{{ c.other_name }}</div>
            <div class="conv-position" v-if="c.position_title">{{ c.position_title }}</div>
            <div class="conv-preview" v-if="c.last_message">{{ (c.last_message.content || '').slice(0, 30) }}...</div>
          </div>
          <el-empty v-if="!loadingConvs && conversations.length === 0" description="暂无会话" />
        </div>
        <div class="message-panel">
          <template v-if="currentConvId">
            <div class="messages" ref="messagesRef">
              <div
                v-for="m in messages"
                :key="m.message_id"
                class="msg-row"
                :class="{ self: m.sender === userStore.userInfo?.user_id }"
              >
                <span class="msg-sender">{{ m.sender_name }}:</span>
                <span class="msg-content">{{ m.content }}</span>
                <span class="msg-time">{{ formatTime(m.created_at) }}</span>
              </div>
              <el-empty v-if="!loadingMsg && messages.length === 0" description="暂无消息" />
            </div>
            <div class="input-row">
              <el-input
                v-model="inputContent"
                type="textarea"
                :rows="2"
                placeholder="输入消息..."
                @keydown.enter.exact.prevent="send"
              />
              <el-button type="primary" :loading="sending" @click="send">发送</el-button>
            </div>
          </template>
          <el-empty v-else description="请从左侧选择会话或从岗位/申请/工时页点击「联系教师」或「联系学生」发起会话" />
        </div>
      </div>
    </el-card>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import { useRoute } from 'vue-router'
import { ElMessage } from 'element-plus'
import { useUserStore } from '@/store/user'
import api from '@/api'

const route = useRoute()
const userStore = useUserStore()

const conversations = ref([])
const loadingConvs = ref(false)
const currentConvId = ref(null)
const messages = ref([])
const loadingMsg = ref(false)
const inputContent = ref('')
const sending = ref(false)
const messagesRef = ref(null)

const loadConversations = async () => {
  loadingConvs.value = true
  try {
    const data = await api.chat.getConversations()
    conversations.value = Array.isArray(data) ? data : (data.results || [])
    const qid = route.query.conversation_id
    if (qid && conversations.value.some(c => String(c.conversation_id) === String(qid))) {
      currentConvId.value = Number(qid)
    } else if (conversations.value.length && !currentConvId.value) {
      currentConvId.value = conversations.value[0].conversation_id
    }
  } catch (e) {
    ElMessage.error('加载会话列表失败')
  } finally {
    loadingConvs.value = false
  }
}

const loadMessages = async () => {
  if (!currentConvId.value) return
  loadingMsg.value = true
  try {
    const data = await api.chat.getMessages(currentConvId.value)
    messages.value = Array.isArray(data) ? data : (data.results || [])
    nextTick(() => {
      if (messagesRef.value) messagesRef.value.scrollTop = messagesRef.value.scrollHeight
    })
  } catch (e) {
    ElMessage.error('加载消息失败')
  } finally {
    loadingMsg.value = false
  }
}

const nextTick = (fn) => setTimeout(fn, 0)

const selectConversation = (c) => {
  currentConvId.value = c.conversation_id
  loadMessages()
}

const send = async () => {
  const content = (inputContent.value || '').trim()
  if (!content || !currentConvId.value) return
  sending.value = true
  try {
    const msg = await api.chat.sendMessage(currentConvId.value, content)
    messages.value.push(msg)
    inputContent.value = ''
    loadConversations()
    nextTick(() => {
      if (messagesRef.value) messagesRef.value.scrollTop = messagesRef.value.scrollHeight
    })
  } catch (e) {
    ElMessage.error('发送失败')
  } finally {
    sending.value = false
  }
}

const formatTime = (str) => {
  if (!str) return ''
  const d = new Date(str)
  return d.toLocaleString('zh-CN', { month: '2-digit', day: '2-digit', hour: '2-digit', minute: '2-digit' })
}

watch(currentConvId, () => loadMessages())

onMounted(() => {
  loadConversations()
  const qid = route.query.conversation_id
  if (qid) currentConvId.value = Number(qid)
})
</script>

<style scoped>
.chat-page { padding: 16px; }
.chat-layout { display: flex; gap: 20px; min-height: 400px; }
.conversation-list { width: 260px; border-right: 1px solid #eee; padding-right: 12px; max-height: 480px; overflow-y: auto; }
.conv-item { padding: 12px; cursor: pointer; border-radius: 8px; margin-bottom: 6px; }
.conv-item:hover, .conv-item.active { background: #f0f7ff; }
.conv-other { font-weight: 600; }
.conv-position { font-size: 12px; color: #888; margin-top: 4px; }
.conv-preview { font-size: 12px; color: #666; margin-top: 4px; }
.message-panel { flex: 1; display: flex; flex-direction: column; min-width: 0; }
.messages { flex: 1; overflow-y: auto; max-height: 360px; padding: 12px; }
.msg-row { margin-bottom: 12px; }
.msg-row.self { text-align: right; }
.msg-sender { font-weight: 600; margin-right: 8px; }
.msg-time { font-size: 12px; color: #999; margin-left: 8px; }
.input-row { display: flex; gap: 12px; align-items: flex-end; padding: 12px 0; }
.input-row .el-input { flex: 1; }
</style>
