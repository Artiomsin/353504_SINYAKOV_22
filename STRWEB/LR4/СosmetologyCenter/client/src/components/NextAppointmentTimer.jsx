import React from 'react';

class NextAppointmentTimer extends React.Component {
  constructor(props) {
    super(props);
    this.state = { secondsLeft: null };
  }

  componentDidMount() {
    this.calc();
    this.interval = setInterval(() => this.calc(), 1000);
  }

  componentWillUnmount() {
    clearInterval(this.interval);
  }

  calc() {
    const { nextDate } = this.props;
    const diff = Math.max(0, Math.floor((new Date(nextDate) - new Date()) / 1000));
    this.setState({ secondsLeft: diff });
  }

  render() {
    return (
      <div className="timer">
        До ближайшей записи: {this.state.secondsLeft} секунд
      </div>
    );
  }
}

// значение по умолчанию для props
NextAppointmentTimer.defaultProps = {
  nextDate: new Date().toISOString()
};

export default NextAppointmentTimer;
