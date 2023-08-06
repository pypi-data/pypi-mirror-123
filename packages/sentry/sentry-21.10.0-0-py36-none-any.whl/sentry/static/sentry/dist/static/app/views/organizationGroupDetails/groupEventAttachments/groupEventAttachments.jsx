Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const react_router_1 = require("react-router");
const pick_1 = (0, tslib_1.__importDefault)(require("lodash/pick"));
const asyncComponent_1 = (0, tslib_1.__importDefault)(require("app/components/asyncComponent"));
const emptyStateWarning_1 = (0, tslib_1.__importDefault)(require("app/components/emptyStateWarning"));
const loadingIndicator_1 = (0, tslib_1.__importDefault)(require("app/components/loadingIndicator"));
const pagination_1 = (0, tslib_1.__importDefault)(require("app/components/pagination"));
const panels_1 = require("app/components/panels");
const locale_1 = require("app/locale");
const groupEventAttachmentsFilter_1 = (0, tslib_1.__importDefault)(require("./groupEventAttachmentsFilter"));
const groupEventAttachmentsTable_1 = (0, tslib_1.__importDefault)(require("./groupEventAttachmentsTable"));
class GroupEventAttachments extends asyncComponent_1.default {
    constructor() {
        super(...arguments);
        this.handleDelete = (deletedAttachmentId) => {
            this.setState(prevState => ({
                deletedAttachments: [...prevState.deletedAttachments, deletedAttachmentId],
            }));
        };
    }
    getDefaultState() {
        return Object.assign(Object.assign({}, super.getDefaultState()), { deletedAttachments: [] });
    }
    getEndpoints() {
        const { params, location } = this.props;
        return [
            [
                'eventAttachments',
                `/issues/${params.groupId}/attachments/`,
                {
                    query: Object.assign(Object.assign({}, (0, pick_1.default)(location.query, ['cursor', 'environment', 'types'])), { limit: 50 }),
                },
            ],
        ];
    }
    renderNoQueryResults() {
        return (<emptyStateWarning_1.default>
        <p>{(0, locale_1.t)('Sorry, no event attachments match your search query.')}</p>
      </emptyStateWarning_1.default>);
    }
    renderEmpty() {
        return (<emptyStateWarning_1.default>
        <p>{(0, locale_1.t)("There don't seem to be any event attachments yet.")}</p>
      </emptyStateWarning_1.default>);
    }
    renderLoading() {
        return this.renderBody();
    }
    renderInnerBody() {
        const { projectSlug, params, location } = this.props;
        const { loading, eventAttachments, deletedAttachments } = this.state;
        if (loading) {
            return <loadingIndicator_1.default />;
        }
        if (eventAttachments.length > 0) {
            return (<groupEventAttachmentsTable_1.default attachments={eventAttachments} orgId={params.orgId} projectId={projectSlug} groupId={params.groupId} onDelete={this.handleDelete} deletedAttachments={deletedAttachments}/>);
        }
        if (location.query.types) {
            return this.renderNoQueryResults();
        }
        return this.renderEmpty();
    }
    renderBody() {
        return (<react_1.Fragment>
        <groupEventAttachmentsFilter_1.default />
        <panels_1.Panel className="event-list">
          <panels_1.PanelBody>{this.renderInnerBody()}</panels_1.PanelBody>
        </panels_1.Panel>
        <pagination_1.default pageLinks={this.state.eventAttachmentsPageLinks}/>
      </react_1.Fragment>);
    }
}
exports.default = (0, react_router_1.withRouter)(GroupEventAttachments);
//# sourceMappingURL=groupEventAttachments.jsx.map