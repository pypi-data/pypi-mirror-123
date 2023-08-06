Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const integrations_1 = require("app/actionCreators/integrations");
const modal_1 = require("app/actionCreators/modal");
const access_1 = (0, tslib_1.__importDefault)(require("app/components/acl/access"));
const button_1 = (0, tslib_1.__importDefault)(require("app/components/button"));
const confirm_1 = (0, tslib_1.__importDefault)(require("app/components/confirm"));
const externalLink_1 = (0, tslib_1.__importDefault)(require("app/components/links/externalLink"));
const panels_1 = require("app/components/panels");
const repositoryEditForm_1 = (0, tslib_1.__importDefault)(require("app/components/repositoryEditForm"));
const tooltip_1 = (0, tslib_1.__importDefault)(require("app/components/tooltip"));
const icons_1 = require("app/icons");
const locale_1 = require("app/locale");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const types_1 = require("app/types");
const withOrganization_1 = (0, tslib_1.__importDefault)(require("app/utils/withOrganization"));
class RepositoryRow extends react_1.Component {
    constructor() {
        super(...arguments);
        this.cancelDelete = () => {
            const { api, orgId, repository, onRepositoryChange } = this.props;
            (0, integrations_1.cancelDeleteRepository)(api, orgId, repository.id).then(data => {
                if (onRepositoryChange) {
                    onRepositoryChange(data);
                }
            }, () => { });
        };
        this.deleteRepo = () => {
            const { api, orgId, repository, onRepositoryChange } = this.props;
            (0, integrations_1.deleteRepository)(api, orgId, repository.id).then(data => {
                if (onRepositoryChange) {
                    onRepositoryChange(data);
                }
            }, () => { });
        };
        this.handleEditRepo = (data) => {
            const { onRepositoryChange } = this.props;
            if (onRepositoryChange) {
                onRepositoryChange(data);
            }
        };
        this.openModal = () => {
            const { repository, orgId } = this.props;
            (0, modal_1.openModal)(({ Body, Header, closeModal }) => (<react_1.Fragment>
        <Header closeButton>{(0, locale_1.t)('Edit Repository')}</Header>
        <Body>
          <repositoryEditForm_1.default orgSlug={orgId} repository={repository} onSubmitSuccess={this.handleEditRepo} closeModal={closeModal} onCancel={closeModal}/>
        </Body>
      </react_1.Fragment>));
        };
    }
    getStatusLabel(repo) {
        switch (repo.status) {
            case types_1.RepositoryStatus.PENDING_DELETION:
                return 'Deletion Queued';
            case types_1.RepositoryStatus.DELETION_IN_PROGRESS:
                return 'Deletion in Progress';
            case types_1.RepositoryStatus.DISABLED:
                return 'Disabled';
            case types_1.RepositoryStatus.HIDDEN:
                return 'Disabled';
            default:
                return null;
        }
    }
    get isActive() {
        return this.props.repository.status === types_1.RepositoryStatus.ACTIVE;
    }
    renderDeleteButton(hasAccess) {
        const { repository } = this.props;
        const isActive = this.isActive;
        return (<tooltip_1.default title={(0, locale_1.t)('You must be an organization owner, manager or admin to remove a repository.')} disabled={hasAccess}>
        <confirm_1.default disabled={!hasAccess || (!isActive && repository.status !== types_1.RepositoryStatus.DISABLED)} onConfirm={this.deleteRepo} message={(0, locale_1.t)('Are you sure you want to remove this repository? All associated commit data will be removed in addition to the repository.')}>
          <StyledButton size="xsmall" icon={<icons_1.IconDelete size="xs"/>} label={(0, locale_1.t)('delete')} disabled={!hasAccess}/>
        </confirm_1.default>
      </tooltip_1.default>);
    }
    render() {
        const { repository, showProvider, organization } = this.props;
        const isActive = this.isActive;
        const isCustomRepo = organization.features.includes('integrations-custom-scm') &&
            repository.provider.id === 'integrations:custom_scm';
        return (<access_1.default access={['org:integrations']}>
        {({ hasAccess }) => (<StyledPanelItem status={repository.status}>
            <RepositoryTitleAndUrl>
              <RepositoryTitle>
                <strong>{repository.name}</strong>
                {!isActive && <small> &mdash; {this.getStatusLabel(repository)}</small>}
                {repository.status === types_1.RepositoryStatus.PENDING_DELETION && (<StyledButton size="xsmall" onClick={this.cancelDelete} disabled={!hasAccess} data-test-id="repo-cancel">
                    {(0, locale_1.t)('Cancel')}
                  </StyledButton>)}
              </RepositoryTitle>
              <div>
                {showProvider && <small>{repository.provider.name}</small>}
                {showProvider && repository.url && <span>&nbsp;&mdash;&nbsp;</span>}
                {repository.url && (<small>
                    <externalLink_1.default href={repository.url}>
                      {repository.url.replace('https://', '')}
                    </externalLink_1.default>
                  </small>)}
              </div>
            </RepositoryTitleAndUrl>
            {isCustomRepo ? (<EditAndDelete>
                <StyledButton size="xsmall" icon={<icons_1.IconEdit size="xs"/>} label={(0, locale_1.t)('edit')} disabled={!hasAccess ||
                        (!isActive && repository.status !== types_1.RepositoryStatus.DISABLED)} onClick={() => this.openModal()}/>
                {this.renderDeleteButton(hasAccess)}
              </EditAndDelete>) : (this.renderDeleteButton(hasAccess))}
          </StyledPanelItem>)}
      </access_1.default>);
    }
}
RepositoryRow.defaultProps = {
    showProvider: false,
};
const StyledPanelItem = (0, styled_1.default)(panels_1.PanelItem) `
  /* shorter top padding because of title lineheight */
  padding: ${(0, space_1.default)(1)} ${(0, space_1.default)(2)} ${(0, space_1.default)(2)};
  justify-content: space-between;
  align-items: center;
  flex: 1;

  ${p => p.status === types_1.RepositoryStatus.DISABLED &&
    `
    filter: grayscale(1);
    opacity: 0.4;
  `};

  &:last-child {
    border-bottom: none;
  }
`;
const StyledButton = (0, styled_1.default)(button_1.default) `
  margin-left: ${(0, space_1.default)(1)};
`;
const RepositoryTitleAndUrl = (0, styled_1.default)('div') `
  display: flex;
  flex-direction: column;
`;
const EditAndDelete = (0, styled_1.default)('div') `
  display: flex;
  margin-left: ${(0, space_1.default)(1)};
`;
const RepositoryTitle = (0, styled_1.default)('div') `
  margin-bottom: ${(0, space_1.default)(1)};
  /* accommodate cancel button height */
  line-height: 26px;
`;
exports.default = (0, withOrganization_1.default)(RepositoryRow);
//# sourceMappingURL=repositoryRow.jsx.map