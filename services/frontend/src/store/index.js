import { createStore } from "vuex";

import notes from './modules/notes';
import users from './modules/users';
import tags from './modules/tags';

export default createStore({
  modules: {
    notes,
    users,
    tags,
  }
});
