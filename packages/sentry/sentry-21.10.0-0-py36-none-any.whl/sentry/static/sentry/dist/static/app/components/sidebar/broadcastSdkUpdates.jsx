Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const groupBy_1 = (0, tslib_1.__importDefault)(require("lodash/groupBy"));
const partition_1 = (0, tslib_1.__importDefault)(require("lodash/partition"));
const projectBadge_1 = (0, tslib_1.__importDefault)(require("app/components/idBadge/projectBadge"));
const tag_1 = (0, tslib_1.__importDefault)(require("app/components/tag"));
const iconWarning_1 = require("app/icons/iconWarning");
const locale_1 = require("app/locale");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const getSdkUpdateSuggestion_1 = (0, tslib_1.__importDefault)(require("app/utils/getSdkUpdateSuggestion"));
const withOrganization_1 = (0, tslib_1.__importDefault)(require("app/utils/withOrganization"));
const withProjects_1 = (0, tslib_1.__importDefault)(require("app/utils/withProjects"));
const withSdkUpdates_1 = (0, tslib_1.__importDefault)(require("app/utils/withSdkUpdates"));
const alert_1 = (0, tslib_1.__importDefault)(require("../alert"));
const collapsible_1 = (0, tslib_1.__importDefault)(require("../collapsible"));
const list_1 = (0, tslib_1.__importDefault)(require("../list"));
const listItem_1 = (0, tslib_1.__importDefault)(require("../list/listItem"));
const sidebarPanelItem_1 = (0, tslib_1.__importDefault)(require("./sidebarPanelItem"));
const flattenSuggestions = (list) => list.reduce((suggestions, sdk) => [...suggestions, ...sdk.suggestions], []);
function BroadcastSdkUpdates({ projects, sdkUpdates, organization }) {
    if (!sdkUpdates) {
        return null;
    }
    // Are there any updates?
    if (!flattenSuggestions(sdkUpdates).length) {
        return null;
    }
    function renderUpdates(projectSdkUpdates) {
        // Group SDK updates by project
        const items = Object.entries((0, groupBy_1.default)(projectSdkUpdates, 'projectId'));
        return items
            .map(([projectId, updates]) => {
            const project = projects.find(p => p.id === projectId);
            if (!project) {
                return null;
            }
            // Updates should only be shown to users who are project members or users who have open membership or org write permission
            const hasPermissionToSeeUpdates = project.isMember ||
                organization.features.includes('open-membership') ||
                organization.access.includes('org:write');
            if (!hasPermissionToSeeUpdates) {
                return null;
            }
            return updates.map(({ sdkName, sdkVersion, suggestions }) => {
                const isDeprecated = suggestions.some(suggestion => suggestion.type === 'changeSdk');
                return (<div key={sdkName}>
              <Header>
                <SdkProjectBadge project={project}/>
                {isDeprecated && <tag_1.default type="warning">{(0, locale_1.t)('Deprecated')}</tag_1.default>}
              </Header>
              <SdkOutdatedVersion>
                {(0, locale_1.tct)('This project is on [current-version]', {
                        ['current-version']: (<OutdatedVersion>{`${sdkName}@v${sdkVersion}`}</OutdatedVersion>),
                    })}
              </SdkOutdatedVersion>
              <StyledList>
                {suggestions.map((suggestion, i) => (<listItem_1.default key={i}>
                    {(0, getSdkUpdateSuggestion_1.default)({
                            sdk: {
                                name: sdkName,
                                version: sdkVersion,
                            },
                            suggestion,
                            shortStyle: true,
                            capitalized: true,
                        })}
                  </listItem_1.default>))}
              </StyledList>
            </div>);
            });
        })
            .filter(item => !!item);
    }
    const [deprecatedRavenSdkUpdates, otherSdkUpdates] = (0, partition_1.default)(sdkUpdates, sdkUpdate => sdkUpdate.sdkName.includes('raven') &&
        sdkUpdate.suggestions.some(suggestion => suggestion.type === 'changeSdk'));
    return (<sidebarPanelItem_1.default hasSeen title={(0, locale_1.t)('Update your SDKs')} message={(0, locale_1.t)('We recommend updating the following SDKs to make sure you’re getting all the data you need.')}>
      {!!deprecatedRavenSdkUpdates.length && (<StyledAlert type="warning" icon={<iconWarning_1.IconWarning />}>
          {(0, locale_1.tct)(`[first-sentence]. Any SDK that has the package name ‘raven’ may be missing data. Migrate to the latest SDK version.`, {
                ['first-sentence']: (0, locale_1.tn)('You have %s project using a deprecated version of the Sentry client', 'You have %s projects using a deprecated version of the Sentry client', deprecatedRavenSdkUpdates.length),
            })}
        </StyledAlert>)}
      <UpdatesList>
        <collapsible_1.default>
          {renderUpdates(deprecatedRavenSdkUpdates)}
          {renderUpdates(otherSdkUpdates)}
        </collapsible_1.default>
      </UpdatesList>
    </sidebarPanelItem_1.default>);
}
exports.default = (0, withSdkUpdates_1.default)((0, withProjects_1.default)((0, withOrganization_1.default)(BroadcastSdkUpdates)));
const UpdatesList = (0, styled_1.default)('div') `
  margin-top: ${(0, space_1.default)(3)};
  display: grid;
  grid-auto-flow: row;
  grid-gap: ${(0, space_1.default)(3)};
`;
const Header = (0, styled_1.default)('div') `
  display: grid;
  grid-template-columns: 1fr auto;
  grid-gap: ${(0, space_1.default)(0.5)};
  margin-bottom: ${(0, space_1.default)(0.25)};
  align-items: center;
`;
const SdkOutdatedVersion = (0, styled_1.default)('div') `
  /* 24px + 8px to be aligned with the SdkProjectBadge data */
  padding-left: calc(24px + ${(0, space_1.default)(1)});
`;
const OutdatedVersion = (0, styled_1.default)('span') `
  color: ${p => p.theme.gray400};
`;
const SdkProjectBadge = (0, styled_1.default)(projectBadge_1.default) `
  font-size: ${p => p.theme.fontSizeExtraLarge};
  line-height: 1;
`;
const StyledAlert = (0, styled_1.default)(alert_1.default) `
  margin-top: ${(0, space_1.default)(2)};
`;
const StyledList = (0, styled_1.default)(list_1.default) `
  /* 24px + 8px to be aligned with the project name
  * displayed by the SdkProjectBadge component */
  padding-left: calc(24px + ${(0, space_1.default)(1)});
`;
//# sourceMappingURL=broadcastSdkUpdates.jsx.map