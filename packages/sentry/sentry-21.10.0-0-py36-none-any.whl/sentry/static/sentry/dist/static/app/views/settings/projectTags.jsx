Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const access_1 = (0, tslib_1.__importDefault)(require("app/components/acl/access"));
const button_1 = (0, tslib_1.__importDefault)(require("app/components/button"));
const confirm_1 = (0, tslib_1.__importDefault)(require("app/components/confirm"));
const externalLink_1 = (0, tslib_1.__importDefault)(require("app/components/links/externalLink"));
const panels_1 = require("app/components/panels");
const icons_1 = require("app/icons");
const locale_1 = require("app/locale");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const routeTitle_1 = (0, tslib_1.__importDefault)(require("app/utils/routeTitle"));
const asyncView_1 = (0, tslib_1.__importDefault)(require("app/views/asyncView"));
const emptyMessage_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/emptyMessage"));
const settingsPageHeader_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/settingsPageHeader"));
const textBlock_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/text/textBlock"));
const permissionAlert_1 = (0, tslib_1.__importDefault)(require("app/views/settings/project/permissionAlert"));
class ProjectTags extends asyncView_1.default {
    constructor() {
        super(...arguments);
        this.handleDelete = (key, idx) => () => (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
            const { params } = this.props;
            const { projectId, orgId } = params;
            try {
                yield this.api.requestPromise(`/projects/${orgId}/${projectId}/tags/${key}/`, {
                    method: 'DELETE',
                });
                const tags = [...this.state.tags];
                tags.splice(idx, 1);
                this.setState({ tags });
            }
            catch (error) {
                this.setState({ error: true, loading: false });
            }
        });
    }
    getDefaultState() {
        return Object.assign(Object.assign({}, super.getDefaultState()), { tags: [] });
    }
    getEndpoints() {
        const { projectId, orgId } = this.props.params;
        return [['tags', `/projects/${orgId}/${projectId}/tags/`]];
    }
    getTitle() {
        const { projectId } = this.props.params;
        return (0, routeTitle_1.default)((0, locale_1.t)('Tags'), projectId, false);
    }
    renderBody() {
        const { tags } = this.state;
        const isEmpty = !tags || !tags.length;
        return (<react_1.Fragment>
        <settingsPageHeader_1.default title={(0, locale_1.t)('Tags')}/>
        <permissionAlert_1.default />

        <textBlock_1.default>
          {(0, locale_1.tct)(`Each event in Sentry may be annotated with various tags (key and value pairs).
                 Learn how to [link:add custom tags].`, {
                link: (<externalLink_1.default href="https://docs.sentry.io/platform-redirect/?next=/enriching-events/tags/"/>),
            })}
        </textBlock_1.default>

        <panels_1.Panel>
          <panels_1.PanelHeader>{(0, locale_1.t)('Tags')}</panels_1.PanelHeader>
          <panels_1.PanelBody>
            {isEmpty ? (<emptyMessage_1.default>
                {(0, locale_1.tct)('There are no tags, [link:learn how to add tags]', {
                    link: (<externalLink_1.default href="https://docs.sentry.io/product/sentry-basics/guides/enrich-data/"/>),
                })}
              </emptyMessage_1.default>) : (<access_1.default access={['project:write']}>
                {({ hasAccess }) => tags.map(({ key, canDelete }, idx) => {
                    const enabled = canDelete && hasAccess;
                    return (<TagPanelItem key={key} data-test-id="tag-row">
                        <TagName>{key}</TagName>
                        <Actions>
                          <confirm_1.default message={(0, locale_1.t)('Are you sure you want to remove this tag?')} onConfirm={this.handleDelete(key, idx)} disabled={!enabled}>
                            <button_1.default size="xsmall" title={enabled
                            ? (0, locale_1.t)('Remove tag')
                            : hasAccess
                                ? (0, locale_1.t)('This tag cannot be deleted.')
                                : (0, locale_1.t)('You do not have permission to remove tags.')} icon={<icons_1.IconDelete size="xs"/>} data-test-id="delete"/>
                          </confirm_1.default>
                        </Actions>
                      </TagPanelItem>);
                })}
              </access_1.default>)}
          </panels_1.PanelBody>
        </panels_1.Panel>
      </react_1.Fragment>);
    }
}
exports.default = ProjectTags;
const TagPanelItem = (0, styled_1.default)(panels_1.PanelItem) `
  padding: 0;
  align-items: center;
`;
const TagName = (0, styled_1.default)('div') `
  flex: 1;
  padding: ${(0, space_1.default)(2)};
`;
const Actions = (0, styled_1.default)('div') `
  display: flex;
  align-items: center;
  padding: ${(0, space_1.default)(2)};
`;
//# sourceMappingURL=projectTags.jsx.map