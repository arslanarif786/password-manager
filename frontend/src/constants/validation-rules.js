const rules = {
  required: (val) => !!val || "Field is required",
  firstNameRequired: (val) => !!val || "First name is required",
  lastNameRequired: (val) => !!val || "Last name is required",
  emailRequired: (val) => !!val || "Email is required",
  passwordRequired: (val) => !!val || "Password is required",
  select_field_required: (v) => v.length > 0 || "Field is required",
  password_length: (val) =>
    (val && val.length >= 6) ||
    "Minimum password length is 6 characters",
  password_max_length: (val) =>
    (val && val.length < 15) ||
    "Maximum password length is 15 characters",
  name_max_length: (val) =>
    (val && val.length <= 30) ||
    "Maximum length is 30 characters",
  email: (val) => {
    if (val) {
      return /^\w+([.-]?\w+)*@\w+([.-]?\w+)*(\.\w{2,})+$/.test(val) || "Invalid email format";
    }
    return true;
  },
};

export default rules;
