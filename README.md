# FerienBot2
This code runs the protection template task performed by FerienBot2 on Simple English Wikipedia.

It is essentially split up into two separate tasks:
* add protection templates to protected pages by reviewing Special:Log/protect
* remove protection templates from pages no longer served by protection by reviewing WP:IPT

## Adding protection templates
The bot only adds protection templates to pages in namespaces 0 (Main), 1 (Talk), 4 (Wikipedia), 5 (Wikipedia talk), 9 (MediaWiki talk), 11 (Template talk), 12 (Help), 13 (Help talk), 14 (Category) and 15 (Category talk), that exist. The protection templates are not automatically added to pages in namespaces 2 and 3 (User and User talk) as users may have specific preferences when it comes to including those templates on their userpages. Pages in the namespace 10 (Template) are ignored by the bot entirely. This is because templates are often imported from the English Wikipedia with these protection templates on. However, the protection often needs to be adjusted for these templates, as high-risk templates should be protected. Therefore, the bot leaves it to administrators to manually review templates and whether protection is needed on a case-by-case basis.

It checks the 50 most recent logs in Special:Log/protect. If any protection template existing on Simple English Wikipedia is present on the page, the page will be skipped. If the page does not contain a protection template, {{pp|small=yes}} will be added to the page. Templates with specific reasons are not added by this bot. If an administrator wishes to provide a protection template with information on the reason, they can do so by adding a specific template immediately after protection rather than having the bot fulfil that task.

## Removing protection templates
The bot removes protection templates to pages in namespaces 0 (Main), 1 (Talk), 2 (User), 3 (User talk), 4 (Wikipedia), 5 (Wikipedia talk), 9 (MediaWiki talk), 11 (Template talk), 12 (Help), 13 (Help talk), 14 (Category) and 15 (Category talk). The protection templates are automatically removed from pages in all namespaces, including 2 (User) as when a page is not protected, the protection template will not appear. Namespace 10 (Template) continues to be ignored for the reasons described above.

It checks the pages given in WP:IPT (Category:Wikipedia pages with incorrect protection templates). Using a list in the code, it removes any protection template on the page, even if it's not the {{pp|small=yes}} that the bot always adds.

Once these two tasks are complete, the bot sleeps for an hour and then follows the cycle again until the program has stopped.
