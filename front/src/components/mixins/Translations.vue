<script>
export default {
  computed: {
    sharedLabels () {
      return {
        fields: {
          privacy_level: {
            label: this.$pgettext('Content/Settings/Dropdown.Label/Noun', 'Activity visibility'),
            help: this.$pgettext('Content/Settings/Dropdown.Help text', 'Determine the visibility level of your activity'),
            choices: {
              me: this.$pgettext('Content/Settings/Dropdown', 'Nobody except me'),
              instance: this.$pgettext('Content/Settings/Dropdown', 'Everyone on this instance'),
              everyone: this.$pgettext('Content/Settings/Dropdown', 'Everyone, across all instances'),
            },
            shortChoices: {
              me: this.$pgettext('Content/Settings/Dropdown/Short', 'Private'),
              instance: this.$pgettext('Content/Settings/Dropdown/Short', 'Instance'),
              everyone: this.$pgettext('Content/Settings/Dropdown/Short', 'Everyone'),
            }
          },
          import_status: {
            detailTitle: this.$pgettext('Content/Library/Link.Title', 'Click to display more information about the import process for this upload'),
            choices: {
              skipped: {
                label: this.$pgettext('Content/Library/*', 'Skipped'),
                help: this.$pgettext('Content/Library/Help text', 'This track is already present in one of your libraries'),
              },
              draft: {
                label: this.$pgettext('Content/Library/*/Short', 'Draft'),
                help: this.$pgettext('Content/Library/Help text', 'This track has been uploaded, but hasn\'t been scheduled for processing yet'),
              },
              pending: {
                label: this.$pgettext('Content/Library/*/Short', 'Pending'),
                help: this.$pgettext('Content/Library/Help text', 'This track has been uploaded, but hasn\'t been processed by the server yet'),
              },
              errored: {
                label: this.$pgettext('Content/Library/Table/Short', 'Errored'),
                help: this.$pgettext('Content/Library/Help text', 'This track could not be processed, please make sure it is tagged correctly'),
              },
              finished: {
                label: this.$pgettext('Content/Library/*', 'Finished'),
                help: this.$pgettext('Content/Library/Help text', 'Imported'),
              },
            }
          },
          report_type: {
            label: this.$pgettext('*/*/*', 'Category'),
            choices: {
              takedown_request: this.$pgettext("Content/Moderation/Dropdown", "Takedown request"),
              invalid_metadata: this.$pgettext("Popup/Import/Error.Label", "Invalid metadata"),
              illegal_content: this.$pgettext("Content/Moderation/Dropdown", "Illegal content"),
              offensive_content: this.$pgettext("Content/Moderation/Dropdown", "Offensive content"),
              other: this.$pgettext("Content/Moderation/Dropdown", "Other"),
            },
          },
          summary: {
            label: this.$pgettext('Content/Account/*', 'Bio'),
          },
          content_category: {
            label: this.$pgettext('Content/*/Dropdown.Label/Noun', 'Content category'),
            choices: {
              podcast: this.$pgettext('Content/*/Dropdown', 'Podcast'),
              music: this.$pgettext('*/*/*', 'Music'),
              other: this.$pgettext('*/*/*', 'Other'),
            },
          }
        },
        filters: {
          creation_date: this.$pgettext('Content/*/*/Noun', 'Creation date'),
          release_date: this.$pgettext('Content/*/*/Noun', 'Release date'),
          accessed_date: this.$pgettext('Content/*/*/Noun', 'Accessed date'),
          first_seen: this.$pgettext('Content/Moderation/Dropdown/Noun', 'First seen date'),
          last_seen: this.$pgettext('Content/Moderation/Dropdown/Noun', 'Last seen date'),
          modification_date: this.$pgettext('Content/Playlist/Dropdown/Noun', 'Modification date'),
          expiration_date: this.$pgettext('Content/Admin/Table.Label/Noun', 'Expiration date'),
          track_title: this.$pgettext('Content/*/Dropdown/Noun', 'Track name'),
          album_title: this.$pgettext('Content/*/Dropdown/Noun', 'Album name'),
          artist_name: this.$pgettext('Content/*/Dropdown/Noun', 'Artist name'),
          name: this.$pgettext('*/*/*/Noun', 'Name'),
          length: this.$pgettext('*/*/*/Noun', 'Length'),
          items_count: this.$pgettext('*/*/*/Noun', 'Items'),
          size: this.$pgettext('Content/*/*/Noun', 'Size'),
          bitrate: this.$pgettext('Content/Track/*/Noun', 'Bitrate'),
          duration: this.$pgettext('Content/*/*', 'Duration'),
          date_joined: this.$pgettext('Content/Admin/Table.Label/Noun', 'Sign-up date'),
          last_activity: this.$pgettext('Content/Profile/Table.Label/Short, Noun (Value is a date)', 'Last activity'),
          username: this.$pgettext('Content/*/*', 'Username'),
          domain: this.$pgettext('Content/Moderation/*/Noun', 'Domain'),
          users: this.$pgettext('*/*/*/Noun', 'Users'),
          received_messages: this.$pgettext('Content/Moderation/*/Noun', 'Received messages'),
          uploads: this.$pgettext('*/*/*', 'Uploads'),
          followers: this.$pgettext('Content/Federation/*/Noun', 'Followers'),
        },
        scopes: {
          profile: {
            label: this.$pgettext('Content/OAuth Scopes/Label', 'Profile'),
            description: this.$pgettext('Content/OAuth Scopes/Paragraph', 'Access to email, username, and profile information'),
          },
          libraries: {
            label: this.$pgettext('Content/OAuth Scopes/Label', 'Libraries and uploads'),
            description: this.$pgettext('Content/OAuth Scopes/Paragraph', 'Access to audio files, libraries, artists, albums and tracks'),
          },
          favorites: {
            label: this.$pgettext('Sidebar/Favorites/List item.Link/Noun', 'Favorites'),
            description: this.$pgettext('Content/OAuth Scopes/Paragraph', 'Access to favorites'),
          },
          listenings: {
            label: this.$pgettext('*/*/*/Noun', 'Listenings'),
            description: this.$pgettext('Content/OAuth Scopes/Paragraph', 'Access to listening history'),
          },
          follows: {
            label: this.$pgettext('Content/OAuth Scopes/Label', 'Follows'),
            description: this.$pgettext('Content/OAuth Scopes/Paragraph', 'Access to follows'),
          },
          playlists: {
            label: this.$pgettext('*/*/*', 'Playlists'),
            description: this.$pgettext('Content/OAuth Scopes/Paragraph', 'Access to playlists'),
          },
          radios: {
            label: this.$pgettext('*/*/*', 'Radios'),
            description: this.$pgettext('Content/OAuth Scopes/Paragraph', 'Access to radios'),
          },
          filters: {
            label: this.$pgettext('Content/Settings/Title/Noun', 'Content filters'),
            description: this.$pgettext('Content/OAuth Scopes/Paragraph', 'Access to content filters'),
          },
          notifications: {
            label: this.$pgettext('*/Notifications/*', 'Notifications'),
            description: this.$pgettext('Content/OAuth Scopes/Paragraph', 'Access to notifications'),
          },
          edits: {
            label: this.$pgettext('*/Admin/*/Noun', 'Edits'),
            description: this.$pgettext('Content/OAuth Scopes/Paragraph', 'Access to edits'),
          }
        }
      }
    }
  }
}
</script>
