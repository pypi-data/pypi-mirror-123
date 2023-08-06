Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const indicator_1 = require("app/actionCreators/indicator");
const asyncComponent_1 = (0, tslib_1.__importDefault)(require("app/components/asyncComponent"));
const avatar_1 = (0, tslib_1.__importDefault)(require("app/components/avatar"));
const eventOrGroupHeader_1 = (0, tslib_1.__importDefault)(require("app/components/eventOrGroupHeader"));
const linkWithConfirmation_1 = (0, tslib_1.__importDefault)(require("app/components/links/linkWithConfirmation"));
const pagination_1 = (0, tslib_1.__importDefault)(require("app/components/pagination"));
const panels_1 = require("app/components/panels");
const tooltip_1 = (0, tslib_1.__importDefault)(require("app/components/tooltip"));
const icons_1 = require("app/icons");
const locale_1 = require("app/locale");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const emptyMessage_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/emptyMessage"));
function GroupTombstoneRow({ data, onUndiscard }) {
    const actor = data.actor;
    return (<panels_1.PanelItem center>
      <StyledBox>
        <eventOrGroupHeader_1.default includeLink={false} hideIcons className="truncate" size="normal" data={data}/>
      </StyledBox>
      <AvatarContainer>
        {actor && (<avatar_1.default user={actor} hasTooltip tooltip={(0, locale_1.t)('Discarded by %s', actor.name || actor.email)}/>)}
      </AvatarContainer>
      <ActionContainer>
        <tooltip_1.default title={(0, locale_1.t)('Undiscard')}>
          <linkWithConfirmation_1.default title={(0, locale_1.t)('Undiscard')} className="group-remove btn btn-default btn-sm" message={(0, locale_1.t)('Undiscarding this issue means that ' +
            'incoming events that match this will no longer be discarded. ' +
            'New incoming events will count toward your event quota ' +
            'and will display on your issues dashboard. ' +
            'Are you sure you wish to continue?')} onConfirm={() => {
            onUndiscard(data.id);
        }}>
            <icons_1.IconDelete className="undiscard"/>
          </linkWithConfirmation_1.default>
        </tooltip_1.default>
      </ActionContainer>
    </panels_1.PanelItem>);
}
class GroupTombstones extends asyncComponent_1.default {
    constructor() {
        super(...arguments);
        this.handleUndiscard = (tombstoneId) => {
            const { orgId, projectId } = this.props;
            const path = `/projects/${orgId}/${projectId}/tombstones/${tombstoneId}/`;
            this.api
                .requestPromise(path, {
                method: 'DELETE',
            })
                .then(() => {
                (0, indicator_1.addSuccessMessage)((0, locale_1.t)('Events similar to these will no longer be filtered'));
                this.fetchData();
            })
                .catch(() => {
                (0, indicator_1.addErrorMessage)((0, locale_1.t)('We were unable to undiscard this issue'));
                this.fetchData();
            });
        };
    }
    getEndpoints() {
        const { orgId, projectId } = this.props;
        return [
            ['tombstones', `/projects/${orgId}/${projectId}/tombstones/`, {}, { paginate: true }],
        ];
    }
    renderEmpty() {
        return (<panels_1.Panel>
        <emptyMessage_1.default>{(0, locale_1.t)('You have no discarded issues')}</emptyMessage_1.default>
      </panels_1.Panel>);
    }
    renderBody() {
        const { tombstones, tombstonesPageLinks } = this.state;
        return tombstones.length ? (<react_1.Fragment>
        <panels_1.Panel>
          {tombstones.map(data => (<GroupTombstoneRow key={data.id} data={data} onUndiscard={this.handleUndiscard}/>))}
        </panels_1.Panel>
        {tombstonesPageLinks && <pagination_1.default pageLinks={tombstonesPageLinks}/>}
      </react_1.Fragment>) : (this.renderEmpty());
    }
}
const StyledBox = (0, styled_1.default)('div') `
  flex: 1;
  align-items: center;
  min-width: 0; /* keep child content from stretching flex item */
`;
const AvatarContainer = (0, styled_1.default)('div') `
  margin: 0 ${(0, space_1.default)(4)};
  width: ${(0, space_1.default)(3)};
`;
const ActionContainer = (0, styled_1.default)('div') `
  width: ${(0, space_1.default)(4)};
`;
exports.default = GroupTombstones;
//# sourceMappingURL=groupTombstones.jsx.map