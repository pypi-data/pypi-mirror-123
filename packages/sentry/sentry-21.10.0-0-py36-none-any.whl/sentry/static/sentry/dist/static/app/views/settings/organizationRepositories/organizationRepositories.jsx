Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const alertLink_1 = (0, tslib_1.__importDefault)(require("app/components/alertLink"));
const button_1 = (0, tslib_1.__importDefault)(require("app/components/button"));
const externalLink_1 = (0, tslib_1.__importDefault)(require("app/components/links/externalLink"));
const panels_1 = require("app/components/panels");
const repositoryRow_1 = (0, tslib_1.__importDefault)(require("app/components/repositoryRow"));
const icons_1 = require("app/icons");
const locale_1 = require("app/locale");
const emptyMessage_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/emptyMessage"));
const settingsPageHeader_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/settingsPageHeader"));
const textBlock_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/text/textBlock"));
const OrganizationRepositories = ({ itemList, onRepositoryChange, api, params }) => {
    const { orgId } = params;
    const hasItemList = itemList && itemList.length > 0;
    return (<div>
      <settingsPageHeader_1.default title={(0, locale_1.t)('Repositories')}/>
      <alertLink_1.default to={`/settings/${orgId}/integrations/`}>
        {(0, locale_1.t)('Want to add a repository to start tracking commits? Install or configure your version control integration here.')}
      </alertLink_1.default>
      {!hasItemList && (<div className="m-b-2">
          <textBlock_1.default>
            {(0, locale_1.t)('Connecting a repository allows Sentry to capture commit data via webhooks. ' +
                'This enables features like suggested assignees and resolving issues via commit message. ' +
                "Once you've connected a repository, you can associate commits with releases via the API.")}
            &nbsp;
            {(0, locale_1.tct)('See our [link:documentation] for more details.', {
                link: <externalLink_1.default href="https://docs.sentry.io/learn/releases/"/>,
            })}
          </textBlock_1.default>
        </div>)}

      {hasItemList ? (<panels_1.Panel>
          <panels_1.PanelHeader>{(0, locale_1.t)('Added Repositories')}</panels_1.PanelHeader>
          <panels_1.PanelBody>
            <div>
              {itemList.map(repo => (<repositoryRow_1.default key={repo.id} repository={repo} api={api} showProvider orgId={orgId} onRepositoryChange={onRepositoryChange}/>))}
            </div>
          </panels_1.PanelBody>
        </panels_1.Panel>) : (<panels_1.Panel>
          <emptyMessage_1.default icon={<icons_1.IconCommit size="xl"/>} title={(0, locale_1.t)('Sentry is better with commit data')} description={(0, locale_1.t)('Adding one or more repositories will enable enhanced releases and the ability to resolve Sentry Issues via git message.')} action={<button_1.default href="https://docs.sentry.io/learn/releases/">
                {(0, locale_1.t)('Learn more')}
              </button_1.default>}/>
        </panels_1.Panel>)}
    </div>);
};
exports.default = OrganizationRepositories;
//# sourceMappingURL=organizationRepositories.jsx.map