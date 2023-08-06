Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const isEqual_1 = (0, tslib_1.__importDefault)(require("lodash/isEqual"));
const alert_1 = (0, tslib_1.__importDefault)(require("app/components/alert"));
const asyncComponent_1 = (0, tslib_1.__importDefault)(require("app/components/asyncComponent"));
const button_1 = (0, tslib_1.__importDefault)(require("app/components/button"));
const count_1 = (0, tslib_1.__importDefault)(require("app/components/count"));
const deviceName_1 = (0, tslib_1.__importDefault)(require("app/components/deviceName"));
const globalSelectionLink_1 = (0, tslib_1.__importDefault)(require("app/components/globalSelectionLink"));
const externalLink_1 = (0, tslib_1.__importDefault)(require("app/components/links/externalLink"));
const utils_1 = require("app/components/organizations/globalSelectionHeader/utils");
const panels_1 = require("app/components/panels");
const version_1 = (0, tslib_1.__importDefault)(require("app/components/version"));
const locale_1 = require("app/locale");
const overflowEllipsis_1 = (0, tslib_1.__importDefault)(require("app/styles/overflowEllipsis"));
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const utils_2 = require("app/utils");
class GroupTags extends asyncComponent_1.default {
    getDefaultState() {
        return Object.assign(Object.assign({}, super.getDefaultState()), { tagList: null });
    }
    getEndpoints() {
        const { group, environments } = this.props;
        return [
            [
                'tagList',
                `/issues/${group.id}/tags/`,
                {
                    query: { environment: environments },
                },
            ],
        ];
    }
    componentDidUpdate(prevProps) {
        if (!(0, isEqual_1.default)(prevProps.environments, this.props.environments)) {
            this.remountComponent();
        }
    }
    renderTags() {
        const { baseUrl, location } = this.props;
        const { tagList } = this.state;
        const alphabeticalTags = (tagList !== null && tagList !== void 0 ? tagList : []).sort((a, b) => a.key.localeCompare(b.key));
        return (<Container>
        {alphabeticalTags.map((tag, tagIdx) => (<TagItem key={tagIdx}>
            <panels_1.Panel>
              <StyledPanelHeader hasButtons>
                <TagHeading>{tag.key}</TagHeading>
                <button_1.default size="small" to={{
                    pathname: `${baseUrl}tags/${tag.key}/`,
                    query: (0, utils_1.extractSelectionParameters)(location.query),
                }}>
                  {(0, locale_1.t)('More Details')}
                </button_1.default>
              </StyledPanelHeader>
              <panels_1.PanelBody withPadding>
                <UnstyledUnorderedList>
                  {tag.topValues.map((tagValue, tagValueIdx) => (<li key={tagValueIdx} data-test-id={tag.key}>
                      <TagBarGlobalSelectionLink to={{
                        pathname: `${baseUrl}events/`,
                        query: {
                            query: tagValue.query || `${tag.key}:"${tagValue.value}"`,
                        },
                    }}>
                        <TagBarBackground widthPercent={(0, utils_2.percent)(tagValue.count, tag.totalValues) + '%'}/>
                        <TagBarLabel>
                          {tag.key === 'release' ? (<version_1.default version={tagValue.name} anchor={false}/>) : (<deviceName_1.default value={tagValue.name}/>)}
                        </TagBarLabel>
                        <TagBarCount>
                          <count_1.default value={tagValue.count}/>
                        </TagBarCount>
                      </TagBarGlobalSelectionLink>
                    </li>))}
                </UnstyledUnorderedList>
              </panels_1.PanelBody>
            </panels_1.Panel>
          </TagItem>))}
      </Container>);
    }
    renderBody() {
        return (<div>
        {this.renderTags()}
        <alert_1.default type="info">
          {(0, locale_1.tct)('Tags are automatically indexed for searching and breakdown charts. Learn how to [link: add custom tags to issues]', {
                link: (<externalLink_1.default href="https://docs.sentry.io/platform-redirect/?next=/enriching-events/tags"/>),
            })}
        </alert_1.default>
      </div>);
    }
}
const Container = (0, styled_1.default)('div') `
  display: flex;
  flex-wrap: wrap;
`;
const StyledPanelHeader = (0, styled_1.default)(panels_1.PanelHeader) `
  text-transform: none;
`;
const TagHeading = (0, styled_1.default)('h5') `
  font-size: ${p => p.theme.fontSizeLarge};
  margin-bottom: 0;
`;
const UnstyledUnorderedList = (0, styled_1.default)('ul') `
  list-style: none;
  padding-left: 0;
  margin-bottom: 0;
`;
const TagItem = (0, styled_1.default)('div') `
  padding: 0 ${(0, space_1.default)(1)};
  width: 50%;
`;
const TagBarBackground = (0, styled_1.default)('div') `
  position: absolute;
  top: 0;
  bottom: 0;
  left: 0;
  background: ${p => p.theme.tagBar};
  border-radius: ${p => p.theme.borderRadius};
  width: ${p => p.widthPercent};
`;
const TagBarGlobalSelectionLink = (0, styled_1.default)(globalSelectionLink_1.default) `
  position: relative;
  display: flex;
  line-height: 2.2;
  color: ${p => p.theme.textColor};
  margin-bottom: ${(0, space_1.default)(0.5)};
  padding: 0 ${(0, space_1.default)(1)};
  background: ${p => p.theme.backgroundSecondary};
  border-radius: ${p => p.theme.borderRadius};
  overflow: hidden;

  &:hover {
    color: ${p => p.theme.textColor};
    text-decoration: underline;
    ${TagBarBackground} {
      background: ${p => p.theme.tagBarHover};
    }
  }
`;
const TagBarLabel = (0, styled_1.default)('div') `
  position: relative;
  flex-grow: 1;
  ${overflowEllipsis_1.default}
`;
const TagBarCount = (0, styled_1.default)('div') `
  position: relative;
  padding-left: ${(0, space_1.default)(2)};
  font-variant-numeric: tabular-nums;
`;
exports.default = GroupTags;
//# sourceMappingURL=groupTags.jsx.map