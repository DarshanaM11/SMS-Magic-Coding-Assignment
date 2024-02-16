from flask import request, jsonify

# 2.2.1 List app Users
@app.route('/users', methods=['GET'])
def list_users():
    username = request.args.get('username')
    if username:
        users = User.query.filter_by(username=username).all()
    else:
        users = User.query.all()
    return jsonify([user.serialize() for user in users])

# 2.2.2 Replace some User fields at once
@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    # Get user from database
    user = User.query.get(user_id)
    if not user:
        return jsonify({'message': 'User not found'}), 404
    
    # Update user fields
    data = request.json
    user.username = data.get('username', user.username)
    # Update other fields similarly
    
    db.session.commit()
    return jsonify({'message': 'User updated successfully'})

# 2.2.3 Create some Client
@app.route('/clients', methods=['POST'])
def create_client():
    data = request.json
    # Validate company not taken by other client
    existing_client = Client.query.filter_by(company_id=data['company_id']).first()
    if existing_client:
        return jsonify({'message': 'Company already taken by another client'}), 400
    
    # Create new client
    new_client = Client(
        name=data['name'],
        email=data['email'],
        phone=data['phone'],
        user_id=data['user_id'],
        company_id=data['company_id']
    )
    db.session.add(new_client)
    db.session.commit()
    return jsonify({'message': 'Client created successfully'})

# 2.2.4 Change any Client field
@app.route('/clients/<int:client_id>', methods=['PATCH'])
def update_client(client_id):
    client = Client.query.get(client_id)
    if not client:
        return jsonify({'message': 'Client not found'}), 404
    
    data = request.json
    for key, value in data.items():
        setattr(client, key, value)
    
    db.session.commit()
    return jsonify({'message': 'Client updated successfully'})
