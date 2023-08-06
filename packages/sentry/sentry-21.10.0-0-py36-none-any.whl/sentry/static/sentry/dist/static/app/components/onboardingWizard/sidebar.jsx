Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const framer_motion_1 = require("framer-motion");
const highlight_top_right_svg_1 = (0, tslib_1.__importDefault)(require("sentry-images/pattern/highlight-top-right.svg"));
const onboardingTasks_1 = require("app/actionCreators/onboardingTasks");
const sidebarPanel_1 = (0, tslib_1.__importDefault)(require("app/components/sidebar/sidebarPanel"));
const tooltip_1 = (0, tslib_1.__importDefault)(require("app/components/tooltip"));
const locale_1 = require("app/locale");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const testableTransition_1 = (0, tslib_1.__importDefault)(require("app/utils/testableTransition"));
const withApi_1 = (0, tslib_1.__importDefault)(require("app/utils/withApi"));
const withOrganization_1 = (0, tslib_1.__importDefault)(require("app/utils/withOrganization"));
const withProjects_1 = (0, tslib_1.__importDefault)(require("app/utils/withProjects"));
const progressHeader_1 = (0, tslib_1.__importDefault)(require("./progressHeader"));
const task_1 = (0, tslib_1.__importDefault)(require("./task"));
const taskConfig_1 = require("./taskConfig");
const utils_1 = require("./utils");
/**
 * How long (in ms) to delay before beginning to mark tasks complete
 */
const INITIAL_MARK_COMPLETE_TIMEOUT = 600;
/**
 * How long (in ms) to delay between marking each unseen task as complete.
 */
const COMPLETION_SEEN_TIMEOUT = 800;
const doTimeout = (timeout) => new Promise(resolve => setTimeout(resolve, timeout));
const Heading = (0, styled_1.default)(framer_motion_1.motion.div) `
  display: flex;
  color: ${p => p.theme.purple300};
  font-size: ${p => p.theme.fontSizeExtraSmall};
  text-transform: uppercase;
  font-weight: 600;
  line-height: 1;
  margin-top: ${(0, space_1.default)(3)};
`;
Heading.defaultProps = {
    layout: true,
    transition: (0, testableTransition_1.default)(),
};
const completeNowHeading = <Heading key="now">{(0, locale_1.t)('The Basics')}</Heading>;
const upcomingTasksHeading = (<Heading key="upcoming">
    <tooltip_1.default containerDisplayMode="block" title={(0, locale_1.t)('Some tasks should be completed before completing these tasks')}>
      {(0, locale_1.t)('Level Up')}
    </tooltip_1.default>
  </Heading>);
const completedTasksHeading = <Heading key="complete">{(0, locale_1.t)('Completed')}</Heading>;
class OnboardingWizardSidebar extends react_1.Component {
    constructor() {
        super(...arguments);
        this.makeTaskUpdater = (status) => (task) => {
            const { api, organization } = this.props;
            (0, onboardingTasks_1.updateOnboardingTask)(api, organization, { task, status, completionSeen: true });
        };
        this.renderItem = (task) => (<AnimatedTaskItem task={task} key={`${task.task}`} onSkip={this.makeTaskUpdater('skipped')} onMarkComplete={this.makeTaskUpdater('complete')}/>);
    }
    componentDidMount() {
        return (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
            // Add a minor delay to marking tasks complete to account for the animation
            // opening of the sidebar panel
            yield doTimeout(INITIAL_MARK_COMPLETE_TIMEOUT);
            this.markTasksAsSeen();
        });
    }
    markTasksAsSeen() {
        return (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
            const unseenTasks = this.segmentedTasks.all
                .filter(task => (0, utils_1.taskIsDone)(task) && !task.completionSeen)
                .map(task => task.task);
            // Incrementally mark tasks as seen. This gives the card completion
            // animations time before we move each task into the completed section.
            for (const task of unseenTasks) {
                yield doTimeout(COMPLETION_SEEN_TIMEOUT);
                const { api, organization } = this.props;
                (0, onboardingTasks_1.updateOnboardingTask)(api, organization, {
                    task,
                    completionSeen: true,
                });
            }
        });
    }
    get segmentedTasks() {
        const { organization, projects } = this.props;
        const all = (0, taskConfig_1.getMergedTasks)({ organization, projects }).filter(task => task.display);
        const active = all.filter(utils_1.findActiveTasks);
        const upcoming = all.filter(utils_1.findUpcomingTasks);
        const complete = all.filter(utils_1.findCompleteTasks);
        return { active, upcoming, complete, all };
    }
    render() {
        const { collapsed, orientation, onClose } = this.props;
        const { all, active, upcoming, complete } = this.segmentedTasks;
        const completeList = (<CompleteList key="complete-group">
        <framer_motion_1.AnimatePresence initial={false}>{complete.map(this.renderItem)}</framer_motion_1.AnimatePresence>
      </CompleteList>);
        const items = [
            active.length > 0 && completeNowHeading,
            ...active.map(this.renderItem),
            upcoming.length > 0 && upcomingTasksHeading,
            ...upcoming.map(this.renderItem),
            complete.length > 0 && completedTasksHeading,
            completeList,
        ];
        return (<TaskSidebarPanel collapsed={collapsed} hidePanel={onClose} orientation={orientation}>
        <TopRight src={highlight_top_right_svg_1.default}/>
        <progressHeader_1.default allTasks={all} completedTasks={complete}/>
        <TaskList>
          <framer_motion_1.AnimatePresence initial={false}>{items}</framer_motion_1.AnimatePresence>
        </TaskList>
      </TaskSidebarPanel>);
    }
}
const TaskSidebarPanel = (0, styled_1.default)(sidebarPanel_1.default) `
  width: 450px;
`;
const AnimatedTaskItem = (0, framer_motion_1.motion)(task_1.default);
AnimatedTaskItem.defaultProps = {
    initial: 'initial',
    animate: 'animate',
    exit: 'exit',
    layout: true,
    variants: {
        initial: {
            opacity: 0,
            y: 40,
        },
        animate: {
            opacity: 1,
            y: 0,
            transition: (0, testableTransition_1.default)({
                delay: 0.8,
                when: 'beforeChildren',
                staggerChildren: 0.3,
            }),
        },
        exit: {
            y: 20,
            z: -10,
            opacity: 0,
            transition: { duration: 0.2 },
        },
    },
};
const TaskList = (0, styled_1.default)('div') `
  display: grid;
  grid-auto-flow: row;
  grid-gap: ${(0, space_1.default)(1)};
  margin: ${(0, space_1.default)(1)} ${(0, space_1.default)(4)} ${(0, space_1.default)(4)} ${(0, space_1.default)(4)};
`;
const CompleteList = (0, styled_1.default)('div') `
  display: grid;
  grid-auto-flow: row;

  > div {
    transition: border-radius 500ms;
  }

  > div:not(:first-of-type) {
    margin-top: -1px;
    border-top-left-radius: 0;
    border-top-right-radius: 0;
  }

  > div:not(:last-of-type) {
    border-bottom-left-radius: 0;
    border-bottom-right-radius: 0;
  }
`;
const TopRight = (0, styled_1.default)('img') `
  position: absolute;
  top: 0;
  right: 0;
  width: 60%;
`;
exports.default = (0, withApi_1.default)((0, withOrganization_1.default)((0, withProjects_1.default)(OnboardingWizardSidebar)));
//# sourceMappingURL=sidebar.jsx.map