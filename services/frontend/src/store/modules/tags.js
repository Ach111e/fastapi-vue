import axios from 'axios';

const state = {
  tags: null,
  tag: null,
  selectedTagId: null
};

const getters = {
  stateTags: state => state.tags,
  stateTag: state => state.tag,
  stateSelectedTagId: state => state.selectedTagId
};

const actions = {
  async createTag({dispatch}, tag) {
    await axios.post('tags', tag);
    await dispatch('getTags');
  },
  async getTags({commit}) {
    let {data} = await axios.get('tags');
    commit('setTags', data);
  },
  async viewTag({commit}, id) {
    let {data} = await axios.get(`tag/${id}`);
    commit('setTag', data);
  },
  // eslint-disable-next-line no-empty-pattern
  async updateTag({}, tag) {
    await axios.patch(`tag/${tag.id}`, tag.form);
  },
  // eslint-disable-next-line no-empty-pattern
  async deleteTag({}, id) {
    await axios.delete(`tag/${id}`);
  },
  selectTag({commit}, tagId) {
    commit('setSelectedTagId', tagId);
  }
};

const mutations = {
  setTags(state, tags){
    state.tags = tags;
  },
  setTag(state, tag){
    state.tag = tag;
  },
  setSelectedTagId(state, tagId){
    state.selectedTagId = tagId;
  }
};

export default {
  state,
  getters,
  actions,
  mutations
};
