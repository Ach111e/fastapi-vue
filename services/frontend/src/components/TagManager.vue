<template>
  <div>
    <section>
      <h2>标签管理</h2>
      <hr/><br/>

      <form @submit.prevent="submit">
        <div class="mb-3">
          <label for="name" class="form-label">标签名称:</label>
          <input type="text" name="name" v-model="form.name" class="form-control" />
        </div>
        <button type="submit" class="btn btn-primary">添加标签</button>
      </form>
    </section>

    <br/><br/>

    <section>
      <h3>现有标签</h3>
      <hr/><br/>

      <div v-if="tags && tags.length">
        <div v-for="tag in tags" :key="tag.id" class="mb-2">
          <span 
            class="badge me-2" 
            :class="isSelected(tag.id) ? 'bg-primary' : 'bg-secondary'"
            style="cursor: pointer; font-size: 1rem; padding: 0.5rem 1rem;"
            @click="selectTag(tag.id)"
          >
            {{ tag.name }}
          </span>
          <button @click="deleteTag(tag.id)" class="btn btn-sm btn-danger">删除</button>
        </div>
      </div>

      <div v-else>
        <p>暂无标签。</p>
      </div>
    </section>
  </div>
</template>

<script>
import { defineComponent } from 'vue';
import { mapGetters, mapActions } from 'vuex';

export default defineComponent({
  name: 'TagManager',
  data() {
    return {
      form: {
        name: '',
      },
    };
  },
  created: function() {
    return this.$store.dispatch('getTags');
  },
  computed: {
    ...mapGetters({ tags: 'stateTags', selectedTagId: 'stateSelectedTagId' }),
  },
  methods: {
    ...mapActions(['createTag', 'getTags', 'deleteTag', 'selectTag', 'getNotes']),
    isSelected(tagId) {
      return this.selectedTagId === tagId;
    },
    async submit() {
      await this.createTag(this.form);
      this.form.name = '';
    },
    async selectTag(tagId) {
      if (this.selectedTagId === tagId) {
        await this.$store.dispatch('selectTag', null);
      } else {
        await this.$store.dispatch('selectTag', tagId);
      }
      await this.getNotes();
    }
  },
});
</script>
