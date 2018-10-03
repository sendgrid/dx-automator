import React from 'react';
import { shallow } from 'enzyme';
import renderer from 'react-test-renderer';


import TasksList from '../TasksList';

const tasks = [
  {
    'active': true,
    'link': 'anshulsinghal.me',
    'id': 1,
    'creator': 'anshul'
  },
  {
    'active': true,
    'link': 'github/sendgrid',
    'id': 2,
    'creator': 'another'
  }
];

test('TasksList renders properly', () => {
  const wrapper = shallow(<TasksList tasks={tasks}/>);
  const element = wrapper.find('Card');
  expect(element.length).toBe(2);
  expect(element.get(0).props.children).toBe('anshul');
});

test('TasksList renders a snapshot properly', () => {
  const tree = renderer.create(<TasksList tasks={tasks}/>).toJSON();
  expect(tree).toMatchSnapshot();
});