<template>
  <section>
    <h1>编辑笔记</h1>
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
</template>

<script>
import { defineComponent } from 'vue';
import { mapGetters, mapActions } from 'vuex';

export default defineComponent({
  name: 'EditNote',
  props: ['id'],
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
    this.GetNote();
    this.$store.dispatch('getTags');
  },
  computed: {
    ...mapGetters({ note: 'stateNote', tags: 'stateTags' }),
  },
  methods: {
    ...mapActions(['updateNote', 'viewNote', 'getTags']),
    async submit() {
    try {
      let note = {
        id: this.id,
        form: this.form,
      };
      await this.updateNote(note);
      this.$router.push({name: 'Note', params:{id: this.note.id}});
    } catch (error) {
      console.log(error);
    }
    },
    async GetNote() {
      try {
        await this.viewNote(this.id);
        this.form.title = this.note.title;
        this.form.content = this.note.content;
        if (this.note.tags && this.note.tags.length) {
          this.form.tags = this.note.tags.map(tag => tag.id);
        }
      } catch (error) {
        console.error(error);
        this.$router.push('/dashboard');
      }
    }
  },
});
</script>
