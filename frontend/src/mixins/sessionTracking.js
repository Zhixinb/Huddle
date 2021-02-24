import dbHelper from '../db'

const sessionTracking = {
    created() {
      this.$_mountTime = Date.now()
    },
    beforeDestroy()  {
      const name = this.$options.name // component name.
      const elapsed = Date.now() - this.$_mountTime
      // send data to API somehow, i.e. through a Store action or simply use axios or sth.
      if (!Number.isNaN(elapsed)) {
          let uid = this.$store.getters.uid
          
          dbHelper.logUserSession(uid, name, elapsed)
        //   console.log("tracking: " + uid + ", " + name + ", time elapsed:" + elapsed)
      }
    }
}

export default sessionTracking