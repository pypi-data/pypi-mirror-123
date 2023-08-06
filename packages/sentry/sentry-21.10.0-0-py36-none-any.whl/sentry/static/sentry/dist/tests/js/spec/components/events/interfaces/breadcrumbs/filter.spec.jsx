Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const enzyme_1 = require("sentry-test/enzyme");
const level_1 = (0, tslib_1.__importDefault)(require("app/components/events/interfaces/breadcrumbs/breadcrumb/level"));
const type_1 = (0, tslib_1.__importDefault)(require("app/components/events/interfaces/breadcrumbs/breadcrumb/type"));
const searchBarActionFilter_1 = (0, tslib_1.__importDefault)(require("app/components/events/interfaces/searchBarAction/searchBarActionFilter"));
const breadcrumbs_1 = require("app/types/breadcrumbs");
const options = {
    ['Types']: [
        {
            id: breadcrumbs_1.BreadcrumbType.HTTP,
            description: 'HTTP request',
            symbol: <type_1.default color="green300" type={breadcrumbs_1.BreadcrumbType.HTTP}/>,
            isChecked: true,
        },
        {
            id: breadcrumbs_1.BreadcrumbType.TRANSACTION,
            description: 'Transaction',
            symbol: <type_1.default color="pink300" type={breadcrumbs_1.BreadcrumbType.TRANSACTION}/>,
            isChecked: true,
        },
        {
            id: breadcrumbs_1.BreadcrumbType.UI,
            description: 'User Action',
            symbol: <type_1.default color="purple300" type={breadcrumbs_1.BreadcrumbType.UI}/>,
            isChecked: true,
        },
        {
            id: breadcrumbs_1.BreadcrumbType.NAVIGATION,
            description: 'Navigation',
            symbol: <type_1.default color="green300" type={breadcrumbs_1.BreadcrumbType.NAVIGATION}/>,
            isChecked: true,
        },
        {
            id: breadcrumbs_1.BreadcrumbType.DEBUG,
            description: 'Debug',
            symbol: <type_1.default color="purple300" type={breadcrumbs_1.BreadcrumbType.DEBUG}/>,
            isChecked: true,
        },
        {
            id: breadcrumbs_1.BreadcrumbType.ERROR,
            description: 'Error',
            symbol: <type_1.default color="red300" type={breadcrumbs_1.BreadcrumbType.ERROR}/>,
            isChecked: true,
        },
    ],
    ['Levels']: [
        {
            id: breadcrumbs_1.BreadcrumbLevelType.INFO,
            symbol: <level_1.default level={breadcrumbs_1.BreadcrumbLevelType.INFO}/>,
            isChecked: true,
        },
        {
            id: breadcrumbs_1.BreadcrumbLevelType.ERROR,
            symbol: <level_1.default level={breadcrumbs_1.BreadcrumbLevelType.ERROR}/>,
            isChecked: true,
        },
    ],
};
describe('SearchBarActionFilter', () => {
    let handleFilter;
    beforeEach(() => {
        handleFilter = jest.fn();
    });
    it('default render', () => {
        const wrapper = (0, enzyme_1.mountWithTheme)(<searchBarActionFilter_1.default options={options} onChange={handleFilter}/>);
        const filterDropdownMenu = wrapper.find('StyledContent');
        // Headers
        const headers = filterDropdownMenu.find('Header');
        expect(headers).toHaveLength(2);
        expect(headers.at(0).text()).toBe('Types');
        expect(headers.at(1).text()).toBe('Levels');
        // Lists
        const lists = filterDropdownMenu.find('StyledList');
        expect(lists).toHaveLength(2);
        expect(lists.at(0).find('StyledListItem')).toHaveLength(6);
        expect(lists.at(1).find('StyledListItem')).toHaveLength(2);
        expect(wrapper).toSnapshot();
    });
    it('Without Options', () => {
        const wrapper = (0, enzyme_1.mountWithTheme)(<searchBarActionFilter_1.default options={{}} onChange={handleFilter}/>);
        expect(wrapper.find('Header').exists()).toBe(false);
        expect(wrapper.find('StyledListItem').exists()).toBe(false);
    });
    it('With Option Type only', () => {
        const { Types } = options;
        const wrapper = (0, enzyme_1.mountWithTheme)(<searchBarActionFilter_1.default options={{ Types }} onChange={handleFilter}/>);
        const filterDropdownMenu = wrapper.find('StyledContent');
        // Header
        const header = filterDropdownMenu.find('Header');
        expect(header).toHaveLength(1);
        expect(header.text()).toBe('Types');
        // List
        const list = filterDropdownMenu.find('StyledList');
        expect(list).toHaveLength(1);
        // List Items
        const listItems = list.find('StyledListItem');
        expect(listItems).toHaveLength(6);
        const firstItem = listItems.at(0);
        expect(firstItem.find('Description').text()).toBe(options.Types[0].description);
        // Check Item
        expect(firstItem.find('[role="checkbox"]').find('CheckboxFancyContent').props().isChecked).toBeTruthy();
        firstItem.simulate('click');
        expect(handleFilter).toHaveBeenCalledTimes(1);
    });
    it('With Option Level only', () => {
        const { Levels } = options;
        const wrapper = (0, enzyme_1.mountWithTheme)(<searchBarActionFilter_1.default options={{ Levels }} onChange={handleFilter}/>);
        const filterDropdownMenu = wrapper.find('StyledContent');
        // Header
        const header = filterDropdownMenu.find('Header');
        expect(header).toHaveLength(1);
        expect(header.text()).toBe('Levels');
        // List
        const list = filterDropdownMenu.find('StyledList');
        expect(list).toHaveLength(1);
        // List Items
        const listItems = list.find('StyledListItem');
        expect(listItems).toHaveLength(2);
        const firstItem = listItems.at(0);
        expect(firstItem.text()).toBe('Info');
        // Check Item
        expect(firstItem.find('[role="checkbox"]').find('CheckboxFancyContent').props().isChecked).toBeTruthy();
        firstItem.simulate('click');
        expect(handleFilter).toHaveBeenCalledTimes(1);
    });
});
//# sourceMappingURL=filter.spec.jsx.map