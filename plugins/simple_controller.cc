#include <gazebo/gazebo.hh>
#include <gazebo/physics/physics.hh>
#include <gazebo/common/common.hh>
#include <ignition/math/Vector3.hh>
#include <iostream>

namespace gazebo
{
  class SimpleController : public ModelPlugin
  {
  public:
    void Load(physics::ModelPtr _model, sdf::ElementPtr)
    {
      this->model = _model;
      this->link = _model->GetLink();
      this->goal = ignition::math::Vector3d(5, 0, 0.05); // goal pad position

      this->updateConnection = event::Events::ConnectWorldUpdateBegin(
        std::bind(&SimpleController::OnUpdate, this));
    }

    void OnUpdate()
    {
      ignition::math::Vector3d pos = this->model->WorldPose().Pos();
      ignition::math::Vector3d diff = this->goal - pos;
      double distance = diff.Length();

      std::cout << "Distance to goal: " << distance << std::endl;
      if (distance > 0.3)
      {
        diff.Normalize();
        ignition::math::Vector3d force = diff * 2.0;
        this->link->AddForce(force);
      }
      else
      {
        // Stop when goal reached
        this->link->SetLinearVel(ignition::math::Vector3d::Zero);
      }
    }

  private:
    physics::ModelPtr model;
    physics::LinkPtr link;
    ignition::math::Vector3d goal;
    event::ConnectionPtr updateConnection;
  };

  GZ_REGISTER_MODEL_PLUGIN(SimpleController)
}

