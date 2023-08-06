Object.defineProperty(exports, "__esModule", { value: true });
exports.IntegrationLink = exports.IssueSyncListElementContainer = void 0;
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const react_1 = require("@emotion/react");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const capitalize_1 = (0, tslib_1.__importDefault)(require("lodash/capitalize"));
const hovercard_1 = (0, tslib_1.__importDefault)(require("app/components/hovercard"));
const icons_1 = require("app/icons");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const callIfFunction_1 = require("app/utils/callIfFunction");
const integrationUtil_1 = require("app/utils/integrationUtil");
class IssueSyncListElement extends React.Component {
    constructor() {
        super(...arguments);
        this.hoverCardRef = React.createRef();
        this.handleDelete = () => {
            (0, callIfFunction_1.callIfFunction)(this.props.onClose, this.props.externalIssueId);
        };
        this.handleIconClick = () => {
            if (this.isLinked()) {
                this.handleDelete();
            }
            else if (this.props.onOpen) {
                this.props.onOpen();
            }
        };
    }
    componentDidUpdate(nextProps) {
        if (this.props.showHoverCard !== nextProps.showHoverCard &&
            nextProps.showHoverCard === undefined) {
            this.hoverCardRef.current && this.hoverCardRef.current.handleToggleOff();
        }
    }
    isLinked() {
        return !!(this.props.externalIssueLink && this.props.externalIssueId);
    }
    getIcon() {
        return (0, integrationUtil_1.getIntegrationIcon)(this.props.integrationType);
    }
    getPrettyName() {
        const type = this.props.integrationType;
        switch (type) {
            case 'gitlab':
                return 'GitLab';
            case 'github':
                return 'GitHub';
            case 'github_enterprise':
                return 'GitHub Enterprise';
            case 'vsts':
                return 'Azure DevOps';
            case 'jira_server':
                return 'Jira Server';
            default:
                return (0, capitalize_1.default)(type);
        }
    }
    getLink() {
        return (<exports.IntegrationLink href={this.props.externalIssueLink || undefined} onClick={!this.isLinked() ? this.props.onOpen : undefined}>
        {this.getText()}
      </exports.IntegrationLink>);
    }
    getText() {
        if (this.props.children) {
            return this.props.children;
        }
        if (this.props.externalIssueDisplayName) {
            return this.props.externalIssueDisplayName;
        }
        if (this.props.externalIssueKey) {
            return this.props.externalIssueKey;
        }
        return `Link ${this.getPrettyName()} Issue`;
    }
    render() {
        return (<exports.IssueSyncListElementContainer>
        <react_1.ClassNames>
          {({ css }) => (<hovercard_1.default ref={this.hoverCardRef} containerClassName={css `
                display: flex;
                align-items: center;
                min-width: 0; /* flex-box overflow workaround */
              `} header={this.props.hoverCardHeader} body={this.props.hoverCardBody} bodyClassName="issue-list-body" show={this.props.showHoverCard}>
              {this.getIcon()}
              {this.getLink()}
            </hovercard_1.default>)}
        </react_1.ClassNames>
        {(this.props.onClose || this.props.onOpen) && (<StyledIcon onClick={this.handleIconClick}>
            {this.isLinked() ? <icons_1.IconClose /> : this.props.onOpen ? <icons_1.IconAdd /> : null}
          </StyledIcon>)}
      </exports.IssueSyncListElementContainer>);
    }
}
exports.IssueSyncListElementContainer = (0, styled_1.default)('div') `
  line-height: 0;
  display: flex;
  align-items: center;
  justify-content: space-between;

  &:not(:last-child) {
    margin-bottom: ${(0, space_1.default)(2)};
  }
`;
exports.IntegrationLink = (0, styled_1.default)('a') `
  text-decoration: none;
  padding-bottom: ${(0, space_1.default)(0.25)};
  margin-left: ${(0, space_1.default)(1)};
  color: ${p => p.theme.textColor};
  border-bottom: 1px solid ${p => p.theme.textColor};
  cursor: pointer;
  line-height: 1;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;

  &,
  &:hover {
    border-bottom: 1px solid ${p => p.theme.blue300};
  }
`;
const StyledIcon = (0, styled_1.default)('span') `
  color: ${p => p.theme.textColor};
  cursor: pointer;
`;
exports.default = IssueSyncListElement;
//# sourceMappingURL=issueSyncListElement.jsx.map