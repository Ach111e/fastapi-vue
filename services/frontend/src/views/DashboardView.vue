<template>
  <div class="row">
    <div class="col-md-3">
      <TagManager />
    </div>
    <div class="col-md-9">
      <section>
        <h1>添加新笔记</h1>
        <hr/><br/>

        <form @submit.prevent="submit">
          <div class="mb-3">
            <label for="title" class="form-label">标题:</label>
            <input type="text" name="title" v-model="form.title" class="form-control" />
          </div>
          <div class="mb-3">
            <label for="content" class="form-label">内容:</label>
            <textarea
              name="content"
              v-model="form.content"
              class="form-control"
            ></textarea>
          </div>
          <div class="mb-3">
            <label class="form-label">标签:</label>
            <div v-if="tags && tags.length">
              <div v-for="tag in tags" :key="tag.id" class="form-check">
                <input 
                  type="checkbox" 
                  :value="tag.id" 
                  v-model="form.tags" 
                  class="form-check-input"
                  :id="'tag-' + tag.id"
                />
                <label :for="'tag-' + tag.id" class="form-check-label">
                  {{ tag.name }}
                </label>
              </div>
            </div>
            <div v-else>
              <p>暂无标签，请先创建标签。</p>
            </div>
          </div>
          <button type="submit" class="btn btn-primary">提交</button>
        </form>
      </section>

      <br/><br/>

      <section>
        <h1>笔记列表</h1>
        <div v-if="selectedTagId">
          <p class="text-muted">当前筛选标签: 
            <span class="badge bg-primary">{{ getTagName(selectedTagId) }}</span>
            <button @click="clearFilter" class="btn btn-sm btn-link">清除筛选</button>
          </p>
        </div>
        <hr/><br/>

        <div v-if="notes && notes.length">
          <div v-for="note in notes" :key="note.id" class="notes mb-3">
            <div class="card">
              <div class="card-body">
                <h5 class="card-title">{{ note.title }}</h5>
                <p class="card-text">{{ note.content }}</p>
                <p class="card-text"><small class="text-muted">作者: {{ note.author.username }}</small></p>
                <div v-if="note.tags && note.tags.length">
                  <span class="text-muted">标签: </span>
                  <span v-for="tag in note.tags" :key="tag.id" class="badge bg-secondary me-1">
                    {{ tag.name }}
                  </span>
                </div>
                <router-link :to="{name: 'Note', params:{id: note.id}}" class="btn btn-primary mt-2">查看</router-link>
              </div>
            </div>
          </div>
        </div>

        <div v-else>
          <p>暂无笔记。</p>
        </div>
      </section>
    </div>
  </div>
</template>

<script>
import { defineComponent } from 'vue';
import { mapGetters, mapActions } from 'vuex';
import TagManager from '@/components/TagManager.vue';

export default defineComponent({
  name: 'Dashboard',
  components: {
    TagManager
  },
  data() {
    return {
      form: {
        title: '',
        content: '',
        tags: []
      },
    };
  },
  created: function() {
    this.$store.dispatch('getNotes');
    this.$store.dispatch('getTags');
  },
  computed: {
    ...mapGetters({ 
      notes: 'stateNotes', 
      tags: 'stateTags',
      selectedTagId: 'stateSelectedTagId'
    }),
  },
  methods: {
    ...mapActions(['createNote', 'getNotes', 'selectTag']),
    async submit() {
      await this.createNote(this.form);
      this.form.title = '';
      this.form.content = '';
      this.form.tags = [];
    },
    getTagName(tagId) {
      const tag = this.tags.find(t => t.id === tagId);
      return tag ? tag.name : '';
    },
    async clearFilter() {
      await this.selectTag(null);
      await this.getNotes();
    }
  },
});
</script>
