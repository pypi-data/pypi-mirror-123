Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const react_router_1 = require("react-router");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const framer_motion_1 = require("framer-motion");
const moment_1 = (0, tslib_1.__importDefault)(require("moment"));
const navigation_1 = require("app/actionCreators/navigation");
const avatar_1 = (0, tslib_1.__importDefault)(require("app/components/avatar"));
const button_1 = (0, tslib_1.__importDefault)(require("app/components/button"));
const card_1 = (0, tslib_1.__importDefault)(require("app/components/card"));
const letterAvatar_1 = (0, tslib_1.__importDefault)(require("app/components/letterAvatar"));
const tooltip_1 = (0, tslib_1.__importDefault)(require("app/components/tooltip"));
const icons_1 = require("app/icons");
const locale_1 = require("app/locale");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const analytics_1 = require("app/utils/analytics");
const testableTransition_1 = (0, tslib_1.__importDefault)(require("app/utils/testableTransition"));
const withOrganization_1 = (0, tslib_1.__importDefault)(require("app/utils/withOrganization"));
const skipConfirm_1 = (0, tslib_1.__importDefault)(require("./skipConfirm"));
const utils_1 = require("./utils");
const recordAnalytics = (task, organization, action) => (0, analytics_1.trackAnalyticsEvent)({
    eventKey: 'onboarding.wizard_clicked',
    eventName: 'Onboarding Wizard Clicked',
    organization_id: organization.id,
    todo_id: task.task,
    todo_title: task.title,
    action,
});
function Task({ router, task, onSkip, onMarkComplete, forwardedRef, organization }) {
    const handleSkip = () => {
        recordAnalytics(task, organization, 'skipped');
        onSkip(task.task);
    };
    const handleClick = (e) => {
        recordAnalytics(task, organization, 'clickthrough');
        e.stopPropagation();
        if (task.actionType === 'external') {
            window.open(task.location, '_blank');
        }
        if (task.actionType === 'action') {
            task.action();
        }
        if (task.actionType === 'app') {
            (0, navigation_1.navigateTo)(`${task.location}?onboardingTask`, router);
        }
    };
    if ((0, utils_1.taskIsDone)(task) && task.completionSeen) {
        const completedOn = (0, moment_1.default)(task.dateCompleted);
        return (<TaskCard ref={forwardedRef} onClick={handleClick}>
        <CompleteTitle>
          <StatusIndicator>
            {task.status === 'complete' && <CompleteIndicator />}
            {task.status === 'skipped' && <SkippedIndicator />}
          </StatusIndicator>
          {task.title}
          <DateCompleted title={completedOn.toString()}>
            {completedOn.fromNow()}
          </DateCompleted>
          {task.user ? (<TaskUserAvatar hasTooltip user={task.user}/>) : (<tooltip_1.default containerDisplayMode="inherit" title={(0, locale_1.t)('No user was associated with completing this task')}>
              <TaskBlankAvatar round/>
            </tooltip_1.default>)}
        </CompleteTitle>
      </TaskCard>);
    }
    const IncompleteMarker = task.requisiteTasks.length > 0 && (<tooltip_1.default containerDisplayMode="block" title={(0, locale_1.tct)('[requisite] before completing this task', {
            requisite: task.requisiteTasks[0].title,
        })}>
      <icons_1.IconLock color="orange400"/>
    </tooltip_1.default>);
    const { SupplementComponent } = task;
    const supplement = SupplementComponent && (<SupplementComponent task={task} onCompleteTask={() => onMarkComplete(task.task)}/>);
    const skipAction = task.skippable && (<skipConfirm_1.default onSkip={handleSkip}>
      {({ skip }) => <StyledIconClose size="xs" onClick={skip}/>}
    </skipConfirm_1.default>);
    return (<TaskCard interactive ref={forwardedRef} onClick={handleClick} data-test-id={task.task}>
      <IncompleteTitle>
        {IncompleteMarker}
        {task.title}
      </IncompleteTitle>
      <Description>{`${task.description}`}</Description>
      {task.requisiteTasks.length === 0 && (<ActionBar>
          {skipAction}
          {supplement}
          {task.status === 'pending' ? (<InProgressIndicator user={task.user}/>) : (<button_1.default priority="primary" size="small">
              {(0, locale_1.t)('Start')}
            </button_1.default>)}
        </ActionBar>)}
    </TaskCard>);
}
const TaskCard = (0, styled_1.default)(card_1.default) `
  position: relative;
  padding: ${(0, space_1.default)(2)} ${(0, space_1.default)(3)};
`;
const IncompleteTitle = (0, styled_1.default)('div') `
  display: grid;
  grid-template-columns: max-content 1fr;
  grid-gap: ${(0, space_1.default)(1)};
  align-items: center;
  font-weight: 600;
`;
const CompleteTitle = (0, styled_1.default)(IncompleteTitle) `
  grid-template-columns: min-content 1fr max-content min-content;
`;
const Description = (0, styled_1.default)('p') `
  font-size: ${p => p.theme.fontSizeSmall};
  color: ${p => p.theme.subText};
  margin: ${(0, space_1.default)(0.5)} 0 0 0;
`;
const ActionBar = (0, styled_1.default)('div') `
  display: flex;
  justify-content: flex-end;
  align-items: flex-end;
  margin-top: ${(0, space_1.default)(1.5)};
`;
const InProgressIndicator = (0, styled_1.default)((_a) => {
    var { user } = _a, props = (0, tslib_1.__rest)(_a, ["user"]);
    return (<div {...props}>
    <tooltip_1.default disabled={!user} containerDisplayMode="flex" title={(0, locale_1.tct)('This task has been started by [user]', {
            user: user === null || user === void 0 ? void 0 : user.name,
        })}>
      <icons_1.IconSync />
    </tooltip_1.default>
    {(0, locale_1.t)('Task in progress...')}
  </div>);
}) `
  font-size: ${p => p.theme.fontSizeMedium};
  font-weight: bold;
  color: ${p => p.theme.orange400};
  display: grid;
  grid-template-columns: max-content max-content;
  align-items: center;
  grid-gap: ${(0, space_1.default)(1)};
`;
const StyledIconClose = (0, styled_1.default)(icons_1.IconClose) `
  position: absolute;
  right: ${(0, space_1.default)(1.5)};
  top: ${(0, space_1.default)(1.5)};
  color: ${p => p.theme.gray300};
`;
const transition = (0, testableTransition_1.default)();
const StatusIndicator = (0, styled_1.default)(framer_motion_1.motion.div) `
  display: flex;
`;
StatusIndicator.defaultProps = {
    variants: {
        initial: { opacity: 0, x: 10 },
        animate: { opacity: 1, x: 0 },
    },
    transition,
};
const CompleteIndicator = (0, styled_1.default)(icons_1.IconCheckmark) ``;
CompleteIndicator.defaultProps = {
    isCircled: true,
    color: 'green300',
};
const SkippedIndicator = (0, styled_1.default)(icons_1.IconClose) ``;
SkippedIndicator.defaultProps = {
    isCircled: true,
    color: 'orange400',
};
const completedItemAnimation = {
    initial: { opacity: 0, x: -10 },
    animate: { opacity: 1, x: 0 },
};
const DateCompleted = (0, styled_1.default)(framer_motion_1.motion.div) `
  color: ${p => p.theme.subText};
  font-size: ${p => p.theme.fontSizeSmall};
  font-weight: 300;
`;
DateCompleted.defaultProps = {
    variants: completedItemAnimation,
    transition,
};
const TaskUserAvatar = (0, framer_motion_1.motion)(avatar_1.default);
TaskUserAvatar.defaultProps = {
    variants: completedItemAnimation,
    transition,
};
const TaskBlankAvatar = (0, styled_1.default)((0, framer_motion_1.motion)(letterAvatar_1.default)) `
  position: unset;
`;
TaskBlankAvatar.defaultProps = {
    variants: completedItemAnimation,
    transition,
};
const WrappedTask = (0, withOrganization_1.default)((0, react_router_1.withRouter)(Task));
exports.default = React.forwardRef((props, ref) => <WrappedTask forwardedRef={ref} {...props}/>);
//# sourceMappingURL=task.jsx.map