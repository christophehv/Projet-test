describe('Authentication Flow', () => {
  beforeEach(() => {
    cy.visit('http://localhost:3000')
  })

  it('should register a new user successfully', () => {
    cy.visit('http://localhost:3000/register')
    
    const username = `testuser${Date.now()}`
    cy.get('input[name="username"]').type(username)
    cy.get('input[name="email"]').type(`${username}@example.com`)
    cy.get('input[name="password"]').type('password123')
    cy.get('button[type="submit"]').click()

    // Should redirect to login
    cy.url().should('include', '/login')
  })

  it('should login successfully with correct credentials', () => {
    cy.visit('http://localhost:3000/login')
    
    cy.get('input[name="username"]').type('admin')
    cy.get('input[name="password"]').type('admin123')
    cy.get('button[type="submit"]').click()

    // Should redirect to users list
    cy.url().should('include', '/users')
  })

  it('should show error with incorrect credentials', () => {
    cy.visit('http://localhost:3000/login')
    
    cy.get('input[name="username"]').type('wronguser')
    cy.get('input[name="password"]').type('wrongpass')
    cy.get('button[type="submit"]').click()

    cy.contains('Invalid credentials')
  })
}) 