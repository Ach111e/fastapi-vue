<template>
  <div v-if="note">
    <p><strong>标题:</strong> {{ note.title }}</p>
    <p><strong>内容:</strong> {{ note.content }}</p>
    <p><strong>作者:</strong> {{ note.author.username }}</p>
    <div v-if="note.tags && note.tags.length">
      <p><strong>标签:</strong> 
        <span v-for="tag in note.tags" :key="tag.id" class="badge bg-secondary me-1">
          {{ tag.name }}
        </span>
      </p>
    </div>

    <div v-if="user.id === note.author.id">
      <p><router-link :to="{name: 'EditNote', params:{id: note.id}}" class="btn btn-primary">编辑</router-link></p>
      <p><button @click="removeNote()" class="btn btn-secondary">删除</button></p>
    </div>
  </div>
</template>


<script>
import { defineComponent } from 'vue';
import { mapGetters, mapActions } from 'vuex';

export default defineComponent({
  name: 'Note',
  props: ['id'],
  async created() {
    try {
      await this.viewNote(this.id);
    } catch (error) {
      console.error(error);
      this.$router.push('/dashboard');
    }
  },
  computed: {
    ...mapGetters({ note: 'stateNote', user: 'stateUser'}),
  },
  methods: {
    ...mapActions(['viewNote', 'deleteNote']),
    async removeNote() {
      try {
        await this.deleteNote(this.id);
        this.$router.push('/dashboard');
      } catch (error) {
        console.error(error);
      }
    }
  },
});
</script>
