Vue.mixin({
    created: function () {
	var myOption = this.$options.myOption
	if (myOption) {
	    console.log(myOption)
	}
    },
    methods: {
	makeToast(variant = null, title=null, content=null) {
            this.$bvToast.toast(`${content || 'contentNull'}`, {
		title: `${title || 'TitleNull'}`,
		variant: variant,
		solid: true
            })
	},
	remove(page, url, key, name) {
		 this.boxConfirm = false;
		 this.$bvModal.msgBoxConfirm('Please confirm that you want to delete this ' + page + ': ' + name, {
		     title: 'Please Confirm',
		     size: 'sm',
		     buttonSize: 'sm',
		     okVariant: 'danger',
		     okTitle: 'YES',
		     cancelTitle: 'NO',
		     footerClass: 'p-2',
		     hideHeaderClose: false,
		     centered: true
		 })
		     .then(value => {
			 if (value == true) {
			     axios
				 .delete('/api/' + url + '/' + key + '/')
				 .then(response => {
				     try { app.getUsers(); } catch(err) { console.log(err); }
				     try { app.getCompanies(); } catch(err) { console.log(err); }
				     app.makeToast('success', 'Success', page + " successfully removed");
				 })
				 .catch(error => {
				     this.makeToast('danger', 'Error', error);
				     return false;
				 })
			 }
		     })
	     },
    }
})
