export const SITE = {
  // Update this before deploy. Using current domain as placeholder.
  website: "https://www.async-let.com/",
  author: "Cameron Cooke",
  profile: "#",
  desc: "Articles about Swift, iOS and indie projects delivered asynchronously await!",
  // Temporary title until you pick a new name
  title: "Async Let",
  ogImage: "astropaper-og.jpg",
  lightAndDarkMode: true,
  postPerIndex: 4,
  postPerPage: 4,
  scheduledPostMargin: 15 * 60 * 1000, // 15 minutes
  showArchives: true,
  showBackButton: true, // show back button in post detail
  editPost: {
    enabled: false,
    text: "Edit page",
    url: "",
  },
  dynamicOgImage: true,
  dir: "ltr", // "rtl" | "auto"
  lang: "en", // html lang code. Set this empty and default will be "en"
  timezone: "Etc/UTC", // Default global timezone (IANA format)
  // Analytics
  gaMeasurementId: "G-SF4FBXKHE3",
} as const;
